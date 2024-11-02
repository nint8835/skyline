import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';
import { type ModelConfiguration } from './util';

interface State {
    user: string | null;
    setUser: (user: string | null) => void;

    modelOptions: ModelConfiguration;

    modelOptionsSetters: {
        setStartYear: (year: number) => void;
        setContributions: (contributions: ModelConfiguration['contributions']) => void;
        setIncludeLabels: (includeLabels: boolean) => void;
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
                start_year: 0,
                contributions: 'all',
            },
            modelOptionsSetters: {
                setStartYear: (year) => {
                    set(
                        (state) => {
                            state.modelOptions.start_year = year;
                        },
                        undefined,
                        'setStartYear',
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
                setIncludeLabels: (includeLabels) => {
                    set(
                        (state) => {
                            state.modelOptions.include_labels = includeLabels;
                        },
                        undefined,
                        'setIncludeLabels',
                    );
                },
            },
        })),
    ),
);
