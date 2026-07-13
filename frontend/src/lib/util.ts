import type { ErrorResponseSchema, GetModelData } from '@/queries/api';
import { clsx, type ClassValue } from 'clsx';
import { toast } from 'sonner';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

function isErrorResponse(error: unknown): error is ErrorResponseSchema {
    return (
        typeof error === 'object' &&
        error !== null &&
        'detail' in error &&
        typeof (error as { detail: unknown }).detail === 'string'
    );
}

export function getErrorMessage(error: unknown) {
    if (error instanceof Error) {
        return error.message;
    }

    if (isErrorResponse(error)) {
        return error.detail;
    }

    return 'An unknown error occurred';
}

export function onQueryError(error: unknown) {
    toast.error(getErrorMessage(error));
}

export type ModelConfiguration = GetModelData['path'] & NonNullable<GetModelData['query']>;

export function getModelUrl(configuration: ModelConfiguration) {
    const { year, ...query } = configuration;

    const url = new URL(`/contributions/model/${year}`, window.location.origin);
    Object.entries(query).forEach(([key, value]) => {
        if (value !== undefined) {
            url.searchParams.append(key, value.valueOf().toString());
        }
    });

    return url.toString();
}
