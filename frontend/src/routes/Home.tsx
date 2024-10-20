import { Viewer } from '@/components/Viewer';
import { GitHubIcon } from '@/icons/GitHub';
import { queryClient } from '@/lib/query';
import { useStore } from '@/lib/state';
import { cn, getModelUrl, onQueryError } from '@/lib/util';
import { useGetYears, useStartImport } from '@/queries/api/skylineComponents';
import { useFloating, useHover, useInteractions, useTransitionStyles } from '@floating-ui/react';
import { Button, Field, Input, Label, Select } from '@headlessui/react';
import { type ChangeEvent, useState } from 'react';

function LoginPrompt() {
    return (
        <div className="flex h-dvh w-dvw flex-col items-center justify-center space-y-4">
            <h1 className="text-4xl font-bold">Skyline</h1>
            <div>Generate 3D models visualizing your GitHub contribution activity.</div>
            <a
                className="flex flex-row space-x-4 rounded-md border-2 border-zinc-400 p-2 transition-colors hover:border-zinc-200 hover:bg-zinc-700"
                href="/auth/login"
            >
                <GitHubIcon className="h-6 w-6 fill-white" /> <span>Login with GitHub</span>
            </a>
        </div>
    );
}

function BottomBar() {
    const {
        modelOptions,
        modelOptionsSetters: { setYear },
    } = useStore();

    const { data: availableYears, isPending: yearsPending } = useGetYears({}, { throwOnError: true });
    const { mutateAsync: importYear, isPending: importPending } = useStartImport({
        onError: onQueryError,
    });

    // Tooltip hooks
    const [importExplanationTooltipOpen, setImportExplanationTooltipOpen] = useState(false);
    const {
        refs: importExplanationTooltipRefs,
        floatingStyles: importExplanationTooltipStyles,
        context: importExplanationTooltipContext,
    } = useFloating({
        open: importExplanationTooltipOpen,
        onOpenChange: setImportExplanationTooltipOpen,
    });
    const { isMounted: importExplanationTooltipIsMounted, styles: importExplanationTooltipTransitionStyles } =
        useTransitionStyles(importExplanationTooltipContext);
    const importExplanationTooltipHover = useHover(importExplanationTooltipContext);
    const {
        getReferenceProps: importExplanationTooltipGetReferenceProps,
        getFloatingProps: importExplanationTooltipGetFloatingProps,
    } = useInteractions([importExplanationTooltipHover]);

    const [importYearSelection, setImportYearSelection] = useState<number | null>(null);

    if (yearsPending || importPending || availableYears === undefined) {
        return (
            <div className="flex h-56 flex-col items-center justify-center bg-zinc-800 md:grid-cols-2">
                <div className="h-24 w-24 animate-spin rounded-full border-r-2 border-emerald-500"></div>
            </div>
        );
    }

    async function handleImport() {
        if (!importYearSelection) {
            return;
        }

        await importYear({ pathParams: { year: importYearSelection } });
        queryClient.invalidateQueries({ queryKey: ['contributions', 'years'] });
        setYear(importYearSelection);
        setImportYearSelection(null);
    }

    return (
        <div className="flex h-fit flex-col items-center bg-zinc-800 p-4 md:grid-cols-2">
            <div className="w-full space-y-4 md:w-1/3">
                <div ref={importExplanationTooltipRefs.setReference} {...importExplanationTooltipGetReferenceProps()}>
                    <Field
                        className={cn(
                            'flex flex-col gap-2 transition-all',
                            !availableYears.length && 'pointer-events-none opacity-50',
                        )}
                    >
                        <Label className="font-semibold">Year</Label>
                        <div className="flex gap-2">
                            <Select
                                className="flex-1 rounded-md bg-zinc-900 p-4"
                                value={modelOptions.year}
                                onChange={(e: ChangeEvent<HTMLSelectElement>) =>
                                    setYear(parseInt(e.target.value, 10) || 0)
                                }
                            >
                                <option>Select a year</option>
                                {availableYears.map((year) => (
                                    <option key={year} value={year}>
                                        {year}
                                    </option>
                                ))}
                            </Select>
                            <a
                                className={cn(
                                    'flex w-1/3 justify-center rounded-md bg-emerald-600 p-4 transition-all hover:bg-emerald-700',
                                    !modelOptions.year && 'pointer-events-none opacity-50',
                                )}
                                href={getModelUrl(modelOptions)}
                            >
                                Download
                            </a>
                        </div>
                    </Field>
                </div>
                {importExplanationTooltipIsMounted && !availableYears.length && (
                    <div
                        ref={importExplanationTooltipRefs.setFloating}
                        style={{ ...importExplanationTooltipStyles, ...importExplanationTooltipTransitionStyles }}
                        {...importExplanationTooltipGetFloatingProps()}
                    >
                        <div className="rounded-md bg-zinc-700 p-2 text-center">
                            You must import your contribution data before you can generate a model.
                        </div>
                    </div>
                )}
                <Field className="flex flex-col gap-2">
                    <Label className="font-semibold">Import a year</Label>
                    <div className="flex gap-2">
                        <Input
                            className="flex-1 rounded-md bg-zinc-900 p-4"
                            type="number"
                            min={2005}
                            max={new Date().getFullYear() - 1}
                            value={importYearSelection || ''}
                            onChange={(e: ChangeEvent<HTMLInputElement>) =>
                                setImportYearSelection(parseInt(e.target.value, 10) || null)
                            }
                        />
                        <Button
                            className="w-1/3 rounded-md bg-violet-600 p-4 transition-colors hover:bg-violet-700"
                            onClick={handleImport}
                        >
                            Import
                        </Button>
                    </div>
                </Field>
            </div>
        </div>
    );
}

export function HomeRoute() {
    const { user } = useStore();
    const year = useStore((state) => state.modelOptions.year);

    return user ? (
        <div className="flex h-dvh w-dvw flex-col">
            <div className="min-h-0 flex-1">{(year || null) && <Viewer />}</div>
            <BottomBar />
        </div>
    ) : (
        <LoginPrompt />
    );
}
