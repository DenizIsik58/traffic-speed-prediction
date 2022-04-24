import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Link from '@mui/material/Link';

function Footer() {
  return (
    <Typography align="center" variant="body2" color="text.secondary">
      {'Copyright © '}
      <Link color="inherit" href="https://www.solita.fi/en/?utm_campaign=EST:+Brand&utm_term=solita&utm_source=adwords&utm_medium=ppc&hsa_kw=solita&hsa_acc=2178929025&hsa_mt=e&hsa_grp=123766618555&hsa_tgt=kwd-334844187&hsa_src=g&hsa_cam=13334249436&hsa_net=adwords&hsa_ad=525097120039&hsa_ver=3&gclid=CjwKCAjwx46TBhBhEiwArA_DjGkFg1kyJ3CtpLSkfP-f0rbJ3jo3TOvLLS8Zl7ZTteTN0Ym4PAUYchoCjbYQAvD_BwE">
        SOLITA
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

export default function StickyFooter() {
  return (

      <Box
        component="footer"
        sx={{
          py: 4,
          px: 2,
          mt: 'auto',
          backgroundColor: (theme) =>
            theme.palette.mode === 'light'
              ? theme.palette.grey[200]
              : theme.palette.grey[800],
        }}
      >
        <Container maxWidth="sm">
          <Typography variant="body1">

          </Typography>
          <Footer />
        </Container>

    </Box>
  );
}