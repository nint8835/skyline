import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';
import { type ModelConfiguration } from './util';

interface State {
    user: string | null;
    setUser: (user: string | null) => void;

    modelOptions: ModelConfiguration;

    modelOptionsSetters: {
        setYear: (year: number) => void;
        setContributions: (contributions: ModelConfiguration['contributions']) => void;
    };
}

export const useStore = create<State>()(
    devtools(
        immer((set) => ({
            user: null,
            setUser: (user) => {
                set(
                    (state) => {
                        state.user = user;
                    },
                    undefined,
                    'setUser',
                );
            },

            modelOptions: {
                year: 0,
                contributions: 'all',
            },
            modelOptionsSetters: {
                setYear: (year) => {
                    set(
                        (state) => {
                            state.modelOptions.year = year;
                        },
                        undefined,
                        'setYear',
                    );
                },
                setContributions: (contributions) => {
                    set(
                        (state) => {
                            state.modelOptions.contributions = contributions;
                        },
                        undefined,
                        'setContributions',
                    );
                },
            },
        })),
    ),
);
