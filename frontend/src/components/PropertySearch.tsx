import { useForm } from "react-hook-form";
import { useNavigate, useSearchParams } from "react-router";

interface SearchForm {
  query: string;
  minPrice: string;
  maxPrice: string;
  propertyType: string;
  bedrooms: string;
  bathrooms: string;
  minArea: string;
  maxArea: string;
  location: string;
}

const propertyTypes = [
  "Any",
  "House",
  "Apartment",
  "Condo",
  "Villa",
  "Land",
  "Commercial",
];

export default function PropertySearch() {
  const navigateTo = useNavigate();
  const [searchParams] = useSearchParams();
  const { register, handleSubmit } = useForm<SearchForm>({
    defaultValues: {
      query: searchParams.get("query") || "",
      minPrice: searchParams.get("min_price") || "",
      maxPrice: searchParams.get("max_price") || "",
      propertyType: searchParams.get("property_type") || "",
      bedrooms: searchParams.get("bedrooms") || "",
      bathrooms: searchParams.get("bathrooms") || "",
      minArea: searchParams.get("min_area") || "",
      maxArea: searchParams.get("max_area") || "",
      location: searchParams.get("location") || "",
    },
  });

  const onSubmit = (data: SearchForm) => {
    const params = new URLSearchParams();

    if (data.query) params.set("query", data.query);
    if (data.minPrice) params.set("min_price", data.minPrice);
    if (data.maxPrice) params.set("max_price", data.maxPrice);
    if (data.propertyType && data.propertyType !== "Any")
      params.set("property_type", data.propertyType);
    if (data.bedrooms) params.set("bedrooms", data.bedrooms);
    if (data.bathrooms) params.set("bathrooms", data.bathrooms);
    if (data.minArea) params.set("min_area", data.minArea);
    if (data.maxArea) params.set("max_area", data.maxArea);
    if (data.location) params.set("location", data.location);

    navigateTo(`/properties?${params.toString()}`);
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="mb-8 rounded-lg bg-white p-6 shadow"
    >
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <div>
          <label
            htmlFor="query"
            className="block text-sm font-medium text-gray-700"
          >
            Search
          </label>
          <input
            type="text"
            id="query"
            {...register("query")}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
            placeholder="Search properties..."
          />
        </div>

        <div>
          <label
            htmlFor="location"
            className="block text-sm font-medium text-gray-700"
          >
            Location
          </label>
          <input
            type="text"
            id="location"
            {...register("location")}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
            placeholder="Enter location"
          />
        </div>

        <div>
          <label
            htmlFor="propertyType"
            className="block text-sm font-medium text-gray-700"
          >
            Property Type
          </label>
          <select
            id="propertyType"
            {...register("propertyType")}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
          >
            {propertyTypes.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label
            htmlFor="bedrooms"
            className="block text-sm font-medium text-gray-700"
          >
            Bedrooms
          </label>
          <select
            id="bedrooms"
            {...register("bedrooms")}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
          >
            <option value="">Any</option>
            {[1, 2, 3, 4, 5].map((num) => (
              <option key={num} value={num}>
                {num}+
              </option>
            ))}
          </select>
        </div>

        <div>
          <label
            htmlFor="minPrice"
            className="block text-sm font-medium text-gray-700"
          >
            Min Price
          </label>
          <input
            type="number"
            id="minPrice"
            {...register("minPrice")}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
            placeholder="Min price"
          />
        </div>

        <div>
          <label
            htmlFor="maxPrice"
            className="block text-sm font-medium text-gray-700"
          >
            Max Price
          </label>
          <input
            type="number"
            id="maxPrice"
            {...register("maxPrice")}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
            placeholder="Max price"
          />
        </div>

        <div>
          <label
            htmlFor="minArea"
            className="block text-sm font-medium text-gray-700"
          >
            Min Area (m²)
          </label>
          <input
            type="number"
            id="minArea"
            {...register("minArea")}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
            placeholder="Min area"
          />
        </div>

        <div>
          <label
            htmlFor="maxArea"
            className="block text-sm font-medium text-gray-700"
          >
            Max Area (m²)
          </label>
          <input
            type="number"
            id="maxArea"
            {...register("maxArea")}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
            placeholder="Max area"
          />
        </div>
      </div>

      <div className="mt-6 flex justify-end">
        <button
          type="submit"
          className="rounded-md bg-primary-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
        >
          Search Properties
        </button>
      </div>
    </form>
  );
}
