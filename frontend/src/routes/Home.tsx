import { Viewer } from '@/components/Viewer';
import { useStore } from '@/lib/state';
import { useGetYears } from '@/queries/api/skylineComponents';
import { Suspense, useState } from 'react';

export function HomeRoute() {
    const { data: availableYears } = useGetYears({});
    const { user } = useStore();
    const [selectedYear, setSelectedYear] = useState<number | undefined>();

    return (
        user &&
        availableYears && (
            <div className="flex h-dvh w-dvw flex-col">
                <div className="flex-1">
                    {selectedYear && (
                        <Suspense fallback={null}>
                            <Viewer key={selectedYear} year={selectedYear} user={user} />
                        </Suspense>
                    )}
                </div>

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
    );
}
