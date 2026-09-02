import { createFileRoute } from "@tanstack/react-router";
import { Deck } from "@/components/deck/deck";

export const Route = createFileRoute("/")({ component: Home });

function Home() {
  return <Deck />;
}
