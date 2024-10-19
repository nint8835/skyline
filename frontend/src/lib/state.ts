import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface State {
    user: string | null;
    setUser: (user: string | null) => void;

    selectedYear: number | undefined;
    setSelectedYear: (year: number | undefined) => void;
}

export const useStore = create<State>()(
    devtools((set) => ({
        user: null,
        setUser: (user) => set({ user }, undefined, 'setUser'),

        selectedYear: undefined,
        setSelectedYear: (selectedYear) => set({ selectedYear }, undefined, 'setSelectedYear'),
    })),
);
