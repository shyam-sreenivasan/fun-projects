import { Button, Box } from '@mui/material';
import { useState } from 'react';

const PageButtons = ({
  page,
  totalPages,
  onPageChange,
  size,
}) => {
  const half = Math.floor(size / 2);
  let start = Math.max(0, page - half);
  let end = start + size;

  if (end > totalPages) {
    end = totalPages;
    start = Math.max(0, end - size);
  }

  // If not enough buttons, adjust dynamically
  let left = start;
  let right = end;

  if (end - start < size) {
    const extra = size - (end - start);
    if (left > 0) {
      left = Math.max(0, left - extra);
    } else if (right < totalPages) {
      right = Math.min(totalPages, right + extra);
    }
  }

  const pageRange = Array.from({ length: right - left }, (_, i) => i + left);
  const handlePageChange = (val) => {
    onPageChange(val);
  }

  return (
    <Box sx={{ display: 'flex', gap: 0.5 }}>
      {pageRange.map((val) => (
        <Button
          key={val}
          onClick={() => handlePageChange(val)}
          size="small"
          variant="text"
          sx={{
            textDecoration: page === val ? 'underline' : 'none',
            fontWeight: page === val ? 'bold' : 'normal',
            minWidth: '32px',
            padding: '2px 4px',
            color: '#222',
          }}
        >
          {val + 1}
        </Button>
      ))}
    </Box>
  );
};

export default PageButtons;
