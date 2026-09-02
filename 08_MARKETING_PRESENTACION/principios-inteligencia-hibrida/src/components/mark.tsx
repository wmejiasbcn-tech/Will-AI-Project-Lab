export function WaiplMark({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 64 64" className={className} aria-hidden="true">
      <circle cx="32" cy="32" r="28" fill="none" stroke="currentColor" strokeWidth="1.1" opacity="0.45" />
      <circle cx="32" cy="32" r="16" fill="none" stroke="currentColor" strokeWidth="1.2" />
      <circle cx="32" cy="32" r="2.4" fill="currentColor" />
    </svg>
  );
}
