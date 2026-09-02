import type { ButtonHTMLAttributes } from "react";
import { useEco } from "@/lib/store";
import { cn } from "@/lib/cn";

export function Term({
  id,
  children,
  className,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { id: string }) {
  const openGlossary = useEco((s) => s.openGlossary);
  return (
    <button
      type="button"
      {...props}
      onClick={(e) => {
        e.stopPropagation();
        props.onClick?.(e);
        openGlossary(id);
      }}
      className={cn(
        "inline underline decoration-gold/50 decoration-dotted underline-offset-4 hover:decoration-gold",
        className,
      )}
    >
      {children}
    </button>
  );
}
