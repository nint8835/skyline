import { queryClient } from '@/lib/query';
import { useStore } from '@/lib/state';
import { getCurrentUser } from '@/queries/api';
import { HomeRoute } from '@/routes/Home';
import { QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { Toaster } from 'sonner';
import { ErrorPage } from './routes/Error';

const router = createBrowserRouter([
    {
        path: '/',
        loader: async () => {
            const { data: currentUser } = await getCurrentUser({ throwOnError: true });
            useStore.getState().setUser(currentUser);

            return currentUser;
        },
        errorElement: <ErrorPage />,
        children: [
            {
                index: true,
                element: <HomeRoute />,
            },
        ],
    },
]);

export function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <RouterProvider router={router} />
            <ReactQueryDevtools initialIsOpen={false} />
            <Toaster richColors />
        </QueryClientProvider>
    );
}
