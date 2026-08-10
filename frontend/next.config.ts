import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',

  basePath: '/million_miles_test',

  images: {
    unoptimized: true,
    remotePatterns: [
      {
        protocol: "https",
        hostname: "images.unsplash.com"
      },
      {
        protocol: "https",
        hostname: "ci.encar.com"
      }
    ]
  }
  
};

export default nextConfig;
