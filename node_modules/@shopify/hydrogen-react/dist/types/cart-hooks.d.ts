import { CartInput } from './storefront-api-types.js';
import type { StorefrontApiResponseOkPartial } from './storefront-api-response.types.js';
export declare function useCartFetch(): <ReturnDataGeneric>({ query, variables, }: {
    query: string;
    variables: Record<string, unknown>;
}) => Promise<StorefrontApiResponseOkPartial<ReturnDataGeneric>>;
export declare function useInstantCheckout(): {
    cart: import("type-fest/source/partial-deep.js").PartialObjectDeep<import("./cart-types.js").CartBase, {
        recurseIntoArrays: true;
    }> | undefined;
    checkoutUrl: string | undefined;
    error: string | undefined;
    createInstantCheckout: (cartInput: CartInput) => Promise<void>;
};
