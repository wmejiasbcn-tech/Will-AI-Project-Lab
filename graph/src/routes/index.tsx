import { createFileRoute } from "@tanstack/react-router";
import { EcoApp } from "@/components/eco-app";

export const Route = createFileRoute("/")({ component: Home });

function Home() {
  return <EcoApp />;
}
