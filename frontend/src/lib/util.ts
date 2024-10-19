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
