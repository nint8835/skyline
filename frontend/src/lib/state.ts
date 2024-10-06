import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface State {
    user: string | null;
    setUser: (user: string | null) => void;
}

export const useStore = create<State>()(
    devtools((set) => ({
        user: null,
        setUser: (user) => set({ user }, undefined, 'setUser'),
    })),
);
