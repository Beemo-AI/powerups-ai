import { useState } from 'react';
import { motion } from 'framer-motion';
import { Search } from 'lucide-react';

// Map of friendly names to internal API names
const blocks = [
  {
    id: 1,
    displayName: 'Google Search', // User-friendly name for display
    internalName: 'google_search', // Internal name for API
    description: 'Search the web for information',
  },
  {
    id: 2,
    displayName: 'Browse Website', // User-friendly name for display
    internalName: 'get_website_url_content', // Internal name for API
    description: 'Read the contents of a webpage',
  },
  {
    id: 3,
    displayName: 'Extract Links to Visit',
    internalName: 'extract_links', // Example internal name
    description: 'Find Useful Links to Visit',
  },
  {
    id: 5,
    displayName: 'More coming soon!',
    internalName: 'coming_soon', // Example internal name
    description: 'Want something? Send me an email :)',
  },
  // Add more blocks as needed
];

export function PowerUpBlocks({
  onActiveBlocksChange,
}: {
  onActiveBlocksChange: (blocks: string[]) => void;
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeBlocks, setActiveBlocks] = useState<number[]>([]);

  const toggleBlock = (id: number) => {
    const newActiveBlocks = activeBlocks.includes(id)
      ? activeBlocks.filter((blockId) => blockId !== id)
      : [...activeBlocks, id];

    setActiveBlocks(newActiveBlocks);

    // Convert active block IDs to internal names and pass to parent
    const activeBlockNames = newActiveBlocks
      .map((id) => blocks.find((block) => block.id === id)?.internalName || '')
      .filter((name) => name);

    onActiveBlocksChange(activeBlockNames);
  };

  const filteredBlocks = blocks.filter((block) =>
    block.displayName.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className='w-1/2 rounded-[1.5rem] p-6'>
      <div className='relative mb-4'>
        <Search className='absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 transform text-[#81FFFE]' />
        <input
          type='text'
          placeholder='Search blocks...'
          className='joyful-input w-full rounded-lg border border-[rgba(255,255,255,0.1)] py-2 pl-10 pr-4'
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>
      <div className='space-y-3'>
        {filteredBlocks.map((block) => (
          <motion.div
            key={block.id}
            className={`cursor-pointer rounded-lg p-4 transition-colors`}
            style={{
              background: activeBlocks.includes(block.id)
                ? 'linear-gradient(90deg, rgba(0, 135, 145, 0.7) 0%, rgba(129, 255, 254, 0.3) 100%)'
                : 'rgba(0, 40, 43, 0.4)',
              backdropFilter: 'blur(8px)',
              boxShadow: activeBlocks.includes(block.id)
                ? '0px 0px 15px rgba(129, 255, 254, 0.3)'
                : 'none',
            }}
            onClick={() => toggleBlock(block.id)}
            whileHover={{ scale: 1.02 }}
            layout
          >
            <h3
              className='font-semibold'
              style={{
                background:
                  'linear-gradient(90deg, rgba(255, 255, 255, 0.80) -9.85%, rgba(129, 255, 254, 0.50) 99.95%)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              {block.displayName}
            </h3>
            <p
              style={{
                background:
                  'linear-gradient(90deg, rgba(255, 255, 255, 0.72) 0%, rgba(255, 255, 255, 0.36) 100%)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
              className='text-sm'
            >
              {block.description}
            </p>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
