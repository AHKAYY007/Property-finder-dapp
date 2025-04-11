import useSWR from "swr";
import { fetcher } from "@/lib/api";
import { Link, useSearchParams } from "react-router";

interface Property {
  id: number;
  title: string;
  description: string;
  price: number;
  currency: string;
  location: string;
  bedrooms: number;
  bathrooms: number;
  area: number;
  images: string[];
  is_listed: boolean;
}

export default function PropertyList() {
  const [searchParams] = useSearchParams();
  const queryString = searchParams.toString();
  const { data: properties, error } = useSWR<Property[]>(
    `/api/v1/properties${queryString ? `?${queryString}` : ""}`,
    fetcher
  );

  if (error) {
    return (
      <div className="text-center text-red-600">
        Failed to load properties. Please try again later.
      </div>
    );
  }

  if (!properties) {
    return <div className="text-center">Loading properties...</div>;
  }

  if (properties.length === 0) {
    return (
      <div className="text-center text-gray-600">
        No properties found matching your criteria.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {properties.map((property) => (
        <Link
          key={property.id}
          to={`/properties/${property.id}`}
          className="group relative overflow-hidden rounded-lg bg-white shadow transition hover:shadow-lg"
        >
          <div className="aspect-w-16 aspect-h-9 relative">
            <img
              src={
                property.images[0]
                  ? `${process.env.NEXT_PUBLIC_IPFS_GATEWAY}/ipfs/${property.images[0]}`
                  : "/placeholder.jpg"
              }
              alt={property.title}
              className="object-cover"
            />
          </div>
          <div className="p-4">
            <h3 className="text-lg font-semibold text-gray-900 group-hover:text-primary-600">
              {property.title}
            </h3>
            <p className="mt-1 text-sm text-gray-500">{property.location}</p>
            <div className="mt-2 flex items-center justify-between">
              <p className="text-lg font-bold text-primary-600">
                {property.price} {property.currency}
              </p>
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <span>{property.bedrooms} beds</span>
                <span>•</span>
                <span>{property.bathrooms} baths</span>
                <span>•</span>
                <span>{property.area} m²</span>
              </div>
            </div>
            {property.is_listed && (
              <div className="mt-2">
                <span className="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-800">
                  Listed for Sale
                </span>
              </div>
            )}
          </div>
        </Link>
      ))}
    </div>
  );
}
