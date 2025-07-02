import { Box, Typography, Button, IconButton } from '@mui/material';
import { ChevronLeft, ChevronRight } from '@mui/icons-material';
import PageControl from './PageControl';
import PageButtons from './PageButtons';
import React, { useEffect, useState } from 'react';
import KeyboardDoubleArrowRightIcon from '@mui/icons-material/KeyboardDoubleArrowRight';
import KeyboardDoubleArrowLeftIcon from '@mui/icons-material/KeyboardDoubleArrowLeft';
import LastPageIcon from '@mui/icons-material/LastPage';
import FirstPageIcon from '@mui/icons-material/FirstPage';

const Paginator = ({ page = 0, totalPages, totalDataRows, currDataRows, pageWidth = 4, onPageChange }) => {
  const handlePageChange = (val) => {
    setCurrPage(val);
  }

  const [currPage, setCurrPage] = useState(page);

  const { pageNum, setPage, prev, next, prevJump, nextJump } = PageControl({
    totalPages,
    pageWidth,
    onPageChange: handlePageChange,
    jump: pageWidth
  });

   const isFirst = () => {return  currPage === 0 };
   const isLast = () => { return currPage >= totalPages - 1};

   useEffect(() => {
    onPageChange(currPage);
   }, [currPage]); 
  
  return (
    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2, flexWrap: 'wrap' }}>
      
      {/* Row Info */}
      <Typography sx={{ flex: 1 }}>
        Displaying {currDataRows} rows out of {totalDataRows}
      </Typography>

      {/* Pagination */}
      <Box sx={{ display: 'flex', gap: 1, alignItems: 'center', flexWrap: 'wrap' }}>
        <IconButton onClick={() => setPage(0)} disabled={isFirst()}>
          <FirstPageIcon/>
        </IconButton>
        <IconButton onClick={() => prevJump(currPage)} disabled={isFirst()}>
          <KeyboardDoubleArrowLeftIcon/>
        </IconButton>
        <IconButton onClick={() => prev(currPage)} disabled={isFirst()}>
          <ChevronLeft/>
        </IconButton>
        <PageButtons page={currPage} totalPages={totalPages} onPageChange={handlePageChange} size={pageWidth}/>
        <IconButton onClick={() => next(currPage)} disabled={isLast()}>
          <ChevronRight/>
        </IconButton>
        <IconButton onClick={() => nextJump(currPage)} disabled={isLast()}>
          <KeyboardDoubleArrowRightIcon/>
        </IconButton>
        <IconButton onClick={() => setPage(totalPages-1)} disabled={isLast()}>
          <LastPageIcon/>
        </IconButton>
      </Box>

      {/* Page Count */}
      <Typography sx={{ flex: 1, textAlign: 'right' }}>
        Page {totalPages === 0 ? 0 : currPage + 1} of {totalPages}
      </Typography>
    </Box>
  );
};

export default Paginator;
