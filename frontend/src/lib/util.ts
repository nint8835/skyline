import type { GetModelQueryParams } from '@/queries/api/skylineComponents';
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

export type ModelConfiguration = GetModelQueryParams;

export function getModelUrl(configuration: ModelConfiguration) {
    const url = new URL(`/contributions/model`, window.location.origin);
    Object.entries(configuration).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
            url.searchParams.append(key, value.toString());
        }
    });

    return url.toString();
}
