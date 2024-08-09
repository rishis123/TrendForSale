"use strict";
Object.defineProperty(exports, Symbol.toStringTag, { value: "Module" });
const React = require("react");
const ShopifyProvider = require("./ShopifyProvider.js");
function useMoney(money) {
  const { countryIsoCode, languageIsoCode } = ShopifyProvider.useShop();
  const locale = languageIsoCode.includes("_") ? languageIsoCode.replace("_", "-") : `${languageIsoCode}-${countryIsoCode}`;
  if (!locale) {
    throw new Error(
      `useMoney(): Unable to get 'locale' from 'useShop()', which means that 'locale' was not passed to '<ShopifyProvider/>'. 'locale' is required for 'useMoney()' to work`
    );
  }
  const amount = parseFloat(money.amount);
  const options = React.useMemo(
    () => ({
      style: "currency",
      currency: money.currencyCode
    }),
    [money.currencyCode]
  );
  const defaultFormatter = useLazyFormatter(locale, options);
  const nameFormatter = useLazyFormatter(locale, {
    ...options,
    currencyDisplay: "name"
  });
  const narrowSymbolFormatter = useLazyFormatter(locale, {
    ...options,
    currencyDisplay: "narrowSymbol"
  });
  const withoutTrailingZerosFormatter = useLazyFormatter(locale, {
    ...options,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  });
  const withoutCurrencyFormatter = useLazyFormatter(locale);
  const withoutTrailingZerosOrCurrencyFormatter = useLazyFormatter(locale, {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  });
  const isPartCurrency = (part) => part.type === "currency";
  const lazyFormatters = React.useMemo(
    () => ({
      original: () => money,
      currencyCode: () => money.currencyCode,
      localizedString: () => defaultFormatter().format(amount),
      parts: () => defaultFormatter().formatToParts(amount),
      withoutTrailingZeros: () => amount % 1 === 0 ? withoutTrailingZerosFormatter().format(amount) : defaultFormatter().format(amount),
      withoutTrailingZerosAndCurrency: () => amount % 1 === 0 ? withoutTrailingZerosOrCurrencyFormatter().format(amount) : withoutCurrencyFormatter().format(amount),
      currencyName: () => {
        var _a;
        return ((_a = nameFormatter().formatToParts(amount).find(isPartCurrency)) == null ? void 0 : _a.value) ?? money.currencyCode;
      },
      // e.g. "US dollars"
      currencySymbol: () => {
        var _a;
        return ((_a = defaultFormatter().formatToParts(amount).find(isPartCurrency)) == null ? void 0 : _a.value) ?? money.currencyCode;
      },
      // e.g. "USD"
      currencyNarrowSymbol: () => {
        var _a;
        return ((_a = narrowSymbolFormatter().formatToParts(amount).find(isPartCurrency)) == null ? void 0 : _a.value) ?? "";
      },
      // e.g. "$"
      amount: () => defaultFormatter().formatToParts(amount).filter(
        (part) => ["decimal", "fraction", "group", "integer", "literal"].includes(
          part.type
        )
      ).map((part) => part.value).join("")
    }),
    [
      money,
      amount,
      nameFormatter,
      defaultFormatter,
      narrowSymbolFormatter,
      withoutCurrencyFormatter,
      withoutTrailingZerosFormatter,
      withoutTrailingZerosOrCurrencyFormatter
    ]
  );
  return React.useMemo(
    () => new Proxy(lazyFormatters, {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-unsafe-call
      get: (target, key) => {
        var _a;
        return (_a = Reflect.get(target, key)) == null ? void 0 : _a.call(null);
      }
    }),
    [lazyFormatters]
  );
}
function useLazyFormatter(locale, options) {
  return React.useMemo(() => {
    let memoized;
    return () => memoized ?? (memoized = new Intl.NumberFormat(locale, options));
  }, [locale, options]);
}
exports.useMoney = useMoney;
//# sourceMappingURL=useMoney.js.map
