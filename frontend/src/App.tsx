import { queryClient } from '@/lib/query';
import { useStore } from '@/lib/state';
import { fetchGetCurrentUser } from '@/queries/api/skylineComponents';
import { HomeRoute } from '@/routes/Home';
import { QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { createBrowserRouter, redirectDocument, RouterProvider } from 'react-router-dom';

const router = createBrowserRouter([
    {
        path: '/',
        loader: async () => {
            const currentUser = await fetchGetCurrentUser({});
            if (!currentUser) {
                return redirectDocument('/auth/login');
            }

            useStore.getState().setUser(currentUser);

            return currentUser;
        },
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
        </QueryClientProvider>
    );
}
