export default function Logo({ size = 32, className = '' }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      className={className}
    >
      <rect width="32" height="32" rx="8" fill="#06b6d4" />

      {/* Connection lines */}
      <line x1="16" y1="10" x2="10" y2="17" stroke="white" strokeWidth="1.4" strokeLinecap="round" opacity="0.7" />
      <line x1="16" y1="10" x2="22" y2="15" stroke="white" strokeWidth="1.4" strokeLinecap="round" opacity="0.7" />
      <line x1="16" y1="10" x2="16" y2="22" stroke="white" strokeWidth="1.4" strokeLinecap="round" opacity="0.7" />
      <line x1="10" y1="17" x2="16" y2="22" stroke="white" strokeWidth="1.4" strokeLinecap="round" opacity="0.5" />
      <line x1="22" y1="15" x2="16" y2="22" stroke="white" strokeWidth="1.4" strokeLinecap="round" opacity="0.5" />

      {/* Nodes */}
      <circle cx="16" cy="10" r="3" fill="white" />
      <circle cx="16" cy="10" r="1.5" fill="#06b6d4" />

      <circle cx="10" cy="17" r="2.2" fill="white" opacity="0.9" />
      <circle cx="10" cy="17" r="1" fill="#06b6d4" />

      <circle cx="22" cy="15" r="2.2" fill="white" opacity="0.9" />
      <circle cx="22" cy="15" r="1" fill="#06b6d4" />

      <circle cx="16" cy="22" r="2.5" fill="white" opacity="0.95" />
      <circle cx="16" cy="22" r="1.2" fill="#06b6d4" />
    </svg>
  )
}
