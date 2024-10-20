import type { GetModelPathParams, GetModelQueryParams } from '@/queries/api/skylineComponents';
import { ErrorResponseSchema } from '@/queries/api/skylineSchemas';
import { clsx, type ClassValue } from 'clsx';
import { toast } from 'sonner';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

export function onQueryError(error: any) {
    const stack = (error as Error).stack as string | ErrorResponseSchema;

    if (typeof stack === 'string') {
        toast.error(stack);
    } else {
        toast.error(stack.detail);
    }
}

export type ModelConfiguration = GetModelPathParams & GetModelQueryParams;

export function getModelUrl(configuration: ModelConfiguration) {
    const { year, ...query } = configuration;

    const url = new URL(`/contributions/model/${year}`, window.location.origin);
    Object.entries(query).forEach(([key, value]) => {
        if (value !== undefined) {
            url.searchParams.append(key, value);
        }
    });

    return url.toString();
}
