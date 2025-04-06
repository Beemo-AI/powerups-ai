import { motion } from 'framer-motion';
import { DivideIcon as LucideIcon } from 'lucide-react';

interface PowerUpCardProps {
  icon: LucideIcon;
  name: string;
  description: string;
  gradient: string;
}

export function PowerUpCard({
  icon: Icon,
  name,
  description,
  gradient,
}: PowerUpCardProps) {
  return (
    <motion.div
      className={`relative flex cursor-pointer flex-col items-center justify-center rounded-[1.5rem] p-6 transition-transform hover:scale-105`}
      whileHover={{ y: -5 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      style={{
        background: 'linear-gradient(179deg, #008791 0.52%, #00282B 99.46%)',
        boxShadow:
          '0px 16px 32px 0px rgba(255, 255, 255, 0.10) inset, 0px 4px 15px rgba(0, 0, 0, 0.2)',
        backdropFilter: 'blur(10px)',
      }}
    >
      <Icon className='mb-4 h-12 w-12 text-white' />
      <h3
        className='mb-2 text-lg font-semibold'
        style={{
          background:
            'linear-gradient(90deg, rgba(255, 255, 255, 0.80) -9.85%, rgba(129, 255, 254, 0.50) 99.95%)',
          backgroundClip: 'text',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
        }}
      >
        {name}
      </h3>
      <p
        className='text-center text-sm'
        style={{
          background:
            'linear-gradient(90deg, rgba(255, 255, 255, 0.72) 0%, rgba(255, 255, 255, 0.36) 100%)',
          backgroundClip: 'text',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
        }}
      >
        {description}
      </p>
    </motion.div>
  );
}
