import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface State {
    user: string;
    setUser: (user: string) => void;
}

export const useStore = create<State>()(
    devtools((set) => ({
        user: '',
        setUser: (user) => set({ user }),
    })),
);
