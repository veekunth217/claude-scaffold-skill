---
name: woocommerce
description: WooCommerce development — products, variations, pricing rules, payment gateways, hooks, cart/checkout customization, WebToffee CSV import/export
version: 1.0.0
author: veekunth217
tags: [woocommerce, wordpress, ecommerce, payment-gateway, hooks, products, cart, checkout, csv, webtoffee]
platforms: [claude-code, cursor, codex]
---

# WooCommerce Skill

WooCommerce store development — from product setup to custom pricing, payment gateways, and checkout customization.

**RULE: Show code plan before generating any hooks or overrides. Wait for GO.**

> **🚧 Status: Stub — implementation pending**
>
> This reference skill has the structure but the snippet content is still being filled in
> (you'll see `<!-- TODO -->` placeholders below). It activates and tells Claude the topic
> exists, but won't yield deep snippets yet.
>
> **Want to help?** Pick any TODO, write the snippet, open a PR. See [CONTRIBUTING.md](../../CONTRIBUTING.md).
> Each contribution moves the skill closer to "Ready" status.

---

## Capabilities

### Product Setup & Variations
<!-- TODO: Simple, variable, grouped, external products via WP-CLI and PHP -->
<!-- TODO: Product attributes, variation pricing matrix -->
<!-- TODO: Product meta, custom fields via ACF + WooCommerce -->
<!-- TODO: Bulk product import/export (WebToffee, WooCommerce native) -->

### Custom Pricing Rules
<!-- TODO: Role-based pricing, quantity discounts -->
<!-- TODO: Dynamic pricing hooks: woocommerce_product_get_price -->
<!-- TODO: Cart-level discounts vs product-level -->

### Payment Gateway Integration
<!-- TODO: Custom gateway class extending WC_Payment_Gateway -->
<!-- TODO: Webhook handling, IPN verification -->
<!-- TODO: Stripe, Razorpay, PayU, Cashfree integration patterns -->
<!-- TODO: Test mode, logging, order status transitions -->

### WooCommerce Hooks
<!-- TODO: Product hooks: woocommerce_before/after_add_to_cart_button -->
<!-- TODO: Cart hooks: woocommerce_cart_contents, woocommerce_cart_total -->
<!-- TODO: Order hooks: woocommerce_checkout_create_order, woocommerce_order_status_changed -->
<!-- TODO: Email hooks: woocommerce_email_order_details -->

### Cart & Checkout Customization
<!-- TODO: Add custom fields to checkout: billing, shipping, order notes -->
<!-- TODO: Conditionally hide/show payment methods -->
<!-- TODO: Custom order validation, minimum order amount -->
<!-- TODO: Block-based checkout customization -->

### WebToffee CSV Import/Export
<!-- TODO: Column mapping for product import, variations handling -->
<!-- TODO: Scheduled exports, filtered exports by category/status -->
<!-- TODO: Order export for accounting, custom field export -->

---

## Common Patterns

### Custom pricing by user role
```php
add_filter( 'woocommerce_product_get_price', function( $price, $product ) {
    if ( current_user_can( 'wholesale_customer' ) ) {
        return $price * 0.8; // 20% discount
    }
    return $price;
}, 10, 2 );
```

### Add custom checkout field
```php
add_action( 'woocommerce_after_order_notes', function( $checkout ) {
    woocommerce_form_field( 'custom_field', [
        'type'        => 'text',
        'class'       => ['form-row-wide'],
        'label'       => __( 'Custom Field' ),
        'placeholder' => __( 'Enter value' ),
        'required'    => false,
    ], $checkout->get_value( 'custom_field' ) );
});

add_action( 'woocommerce_checkout_update_order_meta', function( $order_id ) {
    if ( ! empty( $_POST['custom_field'] ) ) {
        update_post_meta( $order_id, '_custom_field', sanitize_text_field( $_POST['custom_field'] ) );
    }
});
```

### Order status change hook
```php
add_action( 'woocommerce_order_status_changed', function( $order_id, $from, $to, $order ) {
    if ( $to === 'completed' ) {
        // Send custom notification, trigger fulfillment, etc.
    }
}, 10, 4 );
```

<!-- TODO: Add full interactive workflows for each capability above -->
