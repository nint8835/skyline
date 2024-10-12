import { Viewer } from '@/components/Viewer';
import { useStore } from '@/lib/state';
import { useGetYears } from '@/queries/api/skylineComponents';
import { Suspense } from 'react';

export function HomeRoute() {
    const { data: availableYears } = useGetYears({});
    const { user } = useStore();

    return (
        <div className="h-dvh w-dvw">
            {user && availableYears && (
                <Suspense fallback={null}>
                    <Viewer year={availableYears[0]} user={user} />
                </Suspense>
            )}
        </div>
    );
}
