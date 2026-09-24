import type { ButtonHTMLAttributes, HTMLAttributes, ReactNode } from "react";
import { cn } from "@/lib/cn";

export function Holo({
  className,
  strong,
  quiet,
  ...props
}: HTMLAttributes<HTMLDivElement> & { strong?: boolean; quiet?: boolean }) {
  return (
    <div
      className={cn(
        "rounded-[20px]",
        strong ? "holo-strong" : quiet ? "holo-quiet" : "holo",
        className,
      )}
      {...props}
    />
  );
}

export function HoloButton({
  className,
  children,
  active,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { active?: boolean }) {
  return (
    <button
      type="button"
      data-active={active ? "true" : "false"}
      className={cn(
        "inline-flex min-h-11 items-center justify-center gap-2 rounded-[14px] px-4 text-[15px] font-medium tracking-wide text-ink",
        "holo transition-transform duration-150 ease-out active:scale-[0.96]",
        "hover:shadow-[var(--shadow-holo-hover)]",
        "disabled:opacity-40",
        active && "holo-strong",
        className,
      )}
      {...props}
    >
      {children}
    </button>
  );
}

export function SectionLabel({ children }: { children: ReactNode }) {
  return (
    <p className="text-[11px] font-medium uppercase tracking-[0.22em] text-muted">
      {children}
    </p>
  );
}
