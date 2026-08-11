"use client";

import { useQuery } from "@tanstack/react-query";
import Image from "next/image";
import { useState } from "react";
import type { CarCard } from "@/types/car";

type BackendListing = {
  car_id: number;
  brand: string;
  model: string;
  year: string | null;
  mileage: number | null;
  price: number | null;
  photo: string | null;
  detail_url: string;
  updated_at: string | null;
};

type BackendPage = {
  page: number;
  per_page: number;
  total: number;
  items: BackendListing[];
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";
console.log(API_BASE_URL)

function formatPrice(price: number | null): string {
  if (!price) return "Price on request";
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(
    price / 3.67
  );
}

function mapCar(item: BackendListing): CarCard {
  return {
    id: item.car_id,
    title: `${item.brand} ${item.model}`.trim(),
    price: formatPrice(item.price),
    mileage: item.mileage ? `${item.mileage.toLocaleString()} km` : "N/A",
    year: item.year ?? "N/A",
    image:
      item.photo ||
      "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80",
    location: "UAE"
  };
}

async function fetchCars(page: number): Promise<BackendPage> {
  console.log(API_BASE_URL)
  const res = await fetch(`${API_BASE_URL}/api/v1/listings?page=${page}&per_page=20`);
  if (!res.ok) {
    throw new Error("Failed to fetch cars");
  }
  return res.json();
}

export default function HomePage() {
  const [page, setPage] = useState(1);
  const { data, isLoading } = useQuery({
    queryKey: ["cars", page],
    queryFn: () => fetchCars(page)
  });
  const cars = (data?.items ?? []).map(mapCar);
  const hasPrev = page > 1;
  const hasNext = !!data && page * data.per_page < data.total;

  return (
    <main className="mx-auto max-w-7xl px-4 pb-16 pt-6 sm:px-6 lg:px-10">
      <header className="rounded-3xl border border-[#223150] bg-[#0d1528]/80 p-5 shadow-2xl shadow-black/30 backdrop-blur md:p-8">
        <div className="mb-8 flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
          <div className="max-w-2xl">
            <p className="mb-3 inline-flex rounded-full border border-[#385084] px-3 py-1 text-xs text-[#9bc0ff]">
              Premium Pre-Owned Vehicles
            </p>
            <h1 className="text-3xl font-semibold leading-tight md:text-5xl">
              Drive your next car in minutes, not months
            </h1>
            <p className="mt-4 max-w-xl text-sm text-[#9badcf] md:text-base">
              A modern marketplace inspired by Million Miles style UX: clean cards, quick filters,
              trusted listings and transparent prices.
            </p>
          </div>
          <button className="w-full rounded-xl bg-[#5aa8ff] px-6 py-3 text-sm font-semibold text-[#081427] transition hover:bg-[#7ab9ff] md:w-auto">
            Browse all cars
          </button>
        </div>

        <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {[
            ["12k+", "Active listings"],
            ["97%", "Verified sellers"],
            ["24/7", "Support"],
            ["1 hour", "Avg. response time"]
          ].map(([value, label]) => (
            <article key={label} className="rounded-2xl border border-[#25355a] bg-[#0c1730] p-4">
              <p className="text-2xl font-bold text-white">{value}</p>
              <p className="text-xs text-[#94a8cc]">{label}</p>
            </article>
          ))}
        </section>
      </header>

      <section className="mt-10">
        <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
          <h2 className="text-2xl font-semibold md:text-3xl">Handpicked inventory</h2>
          <div className="flex items-center gap-2 text-sm">
            <button
              disabled={!hasPrev}
              onClick={() => setPage((p) => p - 1)}
              className="rounded-full border border-[#2a3b63] px-4 py-2 text-[#9fb1d4] enabled:hover:border-[#4a6296] disabled:opacity-40"
            >
              Prev
            </button>
            <span className="text-[#9fb1d4]">Page {page}</span>
            <button
              disabled={!hasNext}
              onClick={() => setPage((p) => p + 1)}
              className="rounded-full border border-[#2a3b63] px-4 py-2 text-[#9fb1d4] enabled:hover:border-[#4a6296] disabled:opacity-40"
            >
              Next
            </button>
          </div>
        </div>

        {isLoading ? (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="h-72 animate-pulse rounded-2xl bg-[#101a31]" />
            ))}
          </div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {cars.map((car) => (
              <article
                key={car.id}
                className="overflow-hidden rounded-2xl border border-[#233459] bg-[#0c1529] transition hover:-translate-y-0.5 hover:border-[#3f5f97]"
              >
                <div className="relative h-44 w-full">
                  <Image src={car.image} alt={car.title} fill className="object-cover" />
                </div>
                <div className="space-y-2 p-4">
                  <h3 className="line-clamp-2 text-sm font-semibold text-white">{car.title}</h3>
                  <p className="text-lg font-bold text-[#8cc3ff]">{car.price}</p>
                  <div className="flex items-center justify-between text-xs text-[#9eb1d6]">
                    <span>{car.year}</span>
                    <span>{car.mileage}</span>
                  </div>
                  <p className="text-xs text-[#7f91b5]">{car.location}</p>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
