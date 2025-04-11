import PropertySearch from "@/components/PropertySearch";
import PropertyList from "@/components/PropertyList";

export default function PropertiesPage() {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Properties</h1>
        <p className="mt-2 text-gray-600">
          Browse through our collection of properties or use the search to find
          your perfect match.
        </p>
      </div>

      <PropertySearch />
      <PropertyList />
    </div>
  );
}
