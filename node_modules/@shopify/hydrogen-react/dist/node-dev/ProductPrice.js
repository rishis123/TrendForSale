"use strict";
Object.defineProperty(exports, Symbol.toStringTag, { value: "Module" });
const jsxRuntime = require("react/jsx-runtime");
const Money = require("./Money.js");
const flattenConnection = require("./flatten-connection.js");
function ProductPrice(props) {
  var _a, _b, _c, _d, _e, _f;
  const {
    priceType = "regular",
    variantId,
    valueType = "min",
    data: product,
    ...passthroughProps
  } = props;
  if (product == null) {
    throw new Error(`<ProductPrice/> requires a product as the 'data' prop`);
  }
  let price;
  let measurement;
  const variant = variantId ? flattenConnection.flattenConnection((product == null ? void 0 : product.variants) ?? {}).find(
    (variant2) => (variant2 == null ? void 0 : variant2.id) === variantId
  ) ?? null : null;
  if (priceType === "compareAt") {
    if (variantId && variant) {
      if (((_a = variant.compareAtPriceV2) == null ? void 0 : _a.amount) === ((_b = variant.priceV2) == null ? void 0 : _b.amount)) {
        return null;
      }
      price = variant.compareAtPriceV2;
    } else if (valueType === "max") {
      price = (_c = product == null ? void 0 : product.compareAtPriceRange) == null ? void 0 : _c.maxVariantPrice;
    } else {
      price = (_d = product == null ? void 0 : product.compareAtPriceRange) == null ? void 0 : _d.minVariantPrice;
    }
  } else {
    if (variantId && variant) {
      price = variant.priceV2;
      if (valueType === "unit") {
        price = variant.unitPrice;
        measurement = variant.unitPriceMeasurement;
      }
    } else if (valueType === "max") {
      price = (_e = product.priceRange) == null ? void 0 : _e.maxVariantPrice;
    } else {
      price = (_f = product.priceRange) == null ? void 0 : _f.minVariantPrice;
    }
  }
  if (!price) {
    return null;
  }
  if (measurement) {
    return /* @__PURE__ */ jsxRuntime.jsx(Money.Money, { ...passthroughProps, data: price, measurement });
  }
  return /* @__PURE__ */ jsxRuntime.jsx(Money.Money, { ...passthroughProps, data: price });
}
exports.ProductPrice = ProductPrice;
//# sourceMappingURL=ProductPrice.js.map
