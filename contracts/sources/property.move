module property_finder::property {
    use sui::object::{Self, ID, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::url::{Self, Url};
    use sui::coin::{Self, Coin};
    use sui::sui::SUI;
    use sui::event;
    use std::string::{Self, String};
    use std::vector;

    // Error codes
    const ENotOwner: u64 = 0;
    const ENotListed: u64 = 1;
    const EAlreadyListed: u64 = 2;
    const EInvalidPrice: u64 = 3;

    // Property NFT representing a real estate property
    struct Property has key, store {
        id: UID,
        owner: address,
        metadata_url: Url,
        title: String,
        description: String,
        location: String,
        property_type: String,
        bedrooms: u64,
        bathrooms: u64,
        area: u64,
        price: u64,
        is_listed: bool,
    }

    // Events
    struct PropertyMinted has copy, drop {
        property_id: ID,
        owner: address,
        metadata_url: Url,
    }

    struct PropertyListed has copy, drop {
        property_id: ID,
        price: u64,
    }

    struct PropertySold has copy, drop {
        property_id: ID,
        from: address,
        to: address,
        price: u64,
    }

    // Create a new property NFT
    public entry fun mint_property(
        metadata_url: vector<u8>,
        title: vector<u8>,
        description: vector<u8>,
        location: vector<u8>,
        property_type: vector<u8>,
        bedrooms: u64,
        bathrooms: u64,
        area: u64,
        price: u64,
        ctx: &mut TxContext
    ) {
        let sender = tx_context::sender(ctx);
        let id = object::new(ctx);

        let property = Property {
            id,
            owner: sender,
            metadata_url: url::new_unsafe_from_bytes(metadata_url),
            title: string::utf8(title),
            description: string::utf8(description),
            location: string::utf8(location),
            property_type: string::utf8(property_type),
            bedrooms,
            bathrooms,
            area,
            price,
            is_listed: false,
        };

        event::emit(PropertyMinted {
            property_id: object::uid_to_inner(&property.id),
            owner: sender,
            metadata_url: property.metadata_url,
        });

        transfer::transfer(property, sender);
    }

    // List a property for sale
    public entry fun list_property(
        property: &mut Property,
        price: u64,
        ctx: &TxContext
    ) {
        let sender = tx_context::sender(ctx);
        assert!(property.owner == sender, ENotOwner);
        assert!(!property.is_listed, EAlreadyListed);
        assert!(price > 0, EInvalidPrice);

        property.is_listed = true;
        property.price = price;

        event::emit(PropertyListed {
            property_id: object::uid_to_inner(&property.id),
            price,
        });
    }

    // Buy a listed property
    public entry fun buy_property(
        property: &mut Property,
        payment: &mut Coin<SUI>,
        ctx: &mut TxContext
    ) {
        let sender = tx_context::sender(ctx);
        assert!(property.is_listed, ENotListed);
        assert!(coin::value(payment) >= property.price, EInvalidPrice);

        // Transfer payment to the seller
        let seller_payment = coin::split(payment, property.price, ctx);
        transfer::public_transfer(seller_payment, property.owner);

        // Update property ownership
        let previous_owner = property.owner;
        property.owner = sender;
        property.is_listed = false;

        event::emit(PropertySold {
            property_id: object::uid_to_inner(&property.id),
            from: previous_owner,
            to: sender,
            price: property.price,
        });
    }

    // Unlist a property
    public entry fun unlist_property(
        property: &mut Property,
        ctx: &TxContext
    ) {
        let sender = tx_context::sender(ctx);
        assert!(property.owner == sender, ENotOwner);
        assert!(property.is_listed, ENotListed);

        property.is_listed = false;
    }

    // Update property price
    public entry fun update_price(
        property: &mut Property,
        new_price: u64,
        ctx: &TxContext
    ) {
        let sender = tx_context::sender(ctx);
        assert!(property.owner == sender, ENotOwner);
        assert!(new_price > 0, EInvalidPrice);

        property.price = new_price;
    }

    // Getters
    public fun get_owner(property: &Property): address {
        property.owner
    }

    public fun get_price(property: &Property): u64 {
        property.price
    }

    public fun is_listed(property: &Property): bool {
        property.is_listed
    }

    public fun get_metadata_url(property: &Property): &Url {
        &property.metadata_url
    }
} 