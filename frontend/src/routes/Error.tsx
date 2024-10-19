import { type ErrorResponseSchema } from '@/queries/api/skylineSchemas';
import { useRouteError } from 'react-router-dom';

export function ErrorPage() {
    const error = useRouteError() as any;
    console.log(error);

    let message = 'An unknown error occurred';

    if (error instanceof Error) {
        message = error.message;
    } else if ('stack' in error && 'detail' in error.stack) {
        message = (error.stack as ErrorResponseSchema).detail;
    }

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
