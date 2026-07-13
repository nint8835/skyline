import { getErrorMessage } from '@/lib/util';
import { useRouteError } from 'react-router-dom';

export function ErrorPage() {
    const message = getErrorMessage(useRouteError());

    return (
        <div className="flex h-dvh w-dvw flex-col items-center justify-center gap-2">
            <h1 className="text-4xl font-bold">An error occurred</h1>
            <pre className="rounded-md bg-zinc-700 p-2 font-mono">{message}</pre>
            <a href="/" className="mt-6 rounded-md bg-sky-500 p-2 hover:bg-sky-600">
                Go back home and try again
            </a>
        </div>
    );
}
