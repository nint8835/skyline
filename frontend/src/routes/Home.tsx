import { Viewer } from '@/components/Viewer';
import { GitHubIcon } from '@/icons/GitHub';
import { useStore } from '@/lib/state';
import { useGetYears } from '@/queries/api/skylineComponents';
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

function BottomBar({
    selectedYear,
    setSelectedYear,
}: {
    selectedYear: number | undefined;
    setSelectedYear: (year: number | undefined) => void;
}) {
    const { data: availableYears } = useGetYears({});

    const [importYearSelection, setImportYearSelection] = useState<number | undefined>();

    if (!availableYears) {
        // TODO: Better loading UI
        return null;
    }

    return (
        <div className="flex h-fit flex-col items-center bg-zinc-800 p-4 md:grid-cols-2">
            <div className="w-full space-y-4 md:w-1/3">
                <Field className="flex flex-col gap-2">
                    <Label className="font-semibold">Year</Label>
                    <div className="flex gap-2">
                        <Select
                            className="flex-1 rounded-md bg-zinc-900 p-4"
                            value={selectedYear}
                            onChange={(e: ChangeEvent<HTMLSelectElement>) =>
                                setSelectedYear(parseInt(e.target.value, 10) || undefined)
                            }
                        >
                            <option>Select a year</option>
                            {availableYears.map((year) => (
                                <option key={year} value={year}>
                                    {year}
                                </option>
                            ))}
                        </Select>
                        <Button className="w-1/3 rounded-md bg-emerald-600 p-4 transition-colors hover:bg-emerald-700">
                            Download
                        </Button>
                    </div>
                </Field>
                <Field className="flex flex-col gap-2">
                    <Label className="font-semibold">Import a year</Label>
                    <div className="flex gap-2">
                        <Input
                            className="flex-1 rounded-md bg-zinc-900 p-4"
                            type="number"
                            min={2007}
                            max={new Date().getFullYear() - 1}
                            value={importYearSelection}
                            onChange={(e: ChangeEvent<HTMLInputElement>) =>
                                setImportYearSelection(parseInt(e.target.value, 10) || undefined)
                            }
                        />
                        <Button className="w-1/3 rounded-md bg-violet-600 p-4 transition-colors hover:bg-violet-700">
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
    const [selectedYear, setSelectedYear] = useState<number | undefined>();

    return user ? (
        <div className="flex h-dvh w-dvw flex-col">
            <div className="flex-1">{selectedYear && <Viewer year={selectedYear} user={user} />}</div>
            <BottomBar selectedYear={selectedYear} setSelectedYear={setSelectedYear} />
        </div>
    ) : (
        <LoginPrompt />
    );
}
