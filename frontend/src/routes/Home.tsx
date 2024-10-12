import { Viewer } from '@/components/Viewer';
import { GitHubIcon } from '@/icons/GitHub';
import { useStore } from '@/lib/state';
import { useGetYears } from '@/queries/api/skylineComponents';
import { useState } from 'react';

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

export function HomeRoute() {
    const { data: availableYears } = useGetYears({});
    const { user } = useStore();
    const [selectedYear, setSelectedYear] = useState<number | undefined>();

    return user ? (
        availableYears && (
            <div className="flex h-dvh w-dvw flex-col">
                <div className="flex-1">{selectedYear && <Viewer year={selectedYear} user={user} />}</div>

                <div className="h-fit">
                    <select value={selectedYear} onChange={(e) => setSelectedYear(parseInt(e.target.value, 10))}>
                        <option>Select a year</option>
                        {availableYears.map((year) => (
                            <option key={year} value={year}>
                                {year}
                            </option>
                        ))}
                    </select>
                </div>
            </div>
        )
    ) : (
        <LoginPrompt />
    );
}
