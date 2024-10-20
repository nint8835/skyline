import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { type ModelConfiguration } from './util';

interface State {
    user: string | null;
    setUser: (user: string | null) => void;

    modelOptions: ModelConfiguration;

    modelOptionsSetters: {
        setYear: (year: number) => void;
    };
}

export const useStore = create<State>()(
    devtools((set) => ({
        user: null,
        setUser: (user) => set({ user }, undefined, 'setUser'),

        modelOptions: {
            year: 0,
        },
        modelOptionsSetters: {
            setYear: (year) => set({ modelOptions: { year } }, undefined, 'setYear'),
        },
    })),
);
