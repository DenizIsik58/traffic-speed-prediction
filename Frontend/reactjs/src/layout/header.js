import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import About from '../pages/about'
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import logo from '../logos/logo-solita-trans_white.png'
import SettingsIcon from '@mui/icons-material/Settings';
import Map from '../pages/map'
import {NavLink, Route, Router, useHistory, useNavigate}  from "react-router-dom";


import {Checkbox, FormControlLabel, Link, Switch} from "@mui/material";
import mapboxgl from "mapbox-gl";


const pages = ['FinMap', 'About Us', 'FAQ', 'Contact Us'];

const ResponsiveAppBar = () => {
  const [anchorElNav, setAnchorElNav] = React.useState(null);
  const [anchorElUser, setAnchorElUser] = React.useState(null);

  const navigate = useNavigate();

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const handleClick = (PATH) => {
        navigate("/" + PATH);
    }


  return (
    <AppBar sx={{bgcolor: "black"}} elevation={0} position="static" >
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ mr: 2, display: { xs: 'none', md: 'flex', my:2}, width: 60, height: 60, objectFit: "cover"}}
          >
            <img style={{cursor:"pointer"}} onClick={()=> window.location.href='/ '} src={logo} className="" alt="logo" />
          </Typography>

          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } , justifyContent : "center"} }>
            <IconButton
              size="large"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: 'block', md: 'none' },
              }}
            >
              {pages.map((page) => (
                <MenuItem key={page} onClick={handleCloseNavMenu}>

                  <Typography onClick={() => handleClick(page)}  textAlign="center">{page}</Typography>

                </MenuItem>
              ))}
            </Menu>
          </Box >
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{display: { xs: 'flex', md: 'none' }, width: 60, height: 60, objectFit: "cover", position: "fixed"}}
          >
            <img src={logo} className="" alt="logo" />
          </Typography>

          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' }, justifyContent: "center", alignItems:"center" }}>

            {pages.map((page) => (
              <Button
                key={page}
                onClick={() => handleClick(page)}
                sx={{ marginLeft: 10, my: 2, color: 'white', display: 'block' }}
              >
                {page}
              </Button>
            ))}
          </Box>

          <Box sx={{ flexGrow: 0 }}>
            <Tooltip title="Open settings">
              <SettingsIcon onClick={handleOpenUserMenu} sx={{ p: 0 }}>
              </SettingsIcon>
            </Tooltip>
            <Menu
              sx={{ mt: '45px' }}
              id="menu-appbar"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
            >
                <MenuItem key="Dark Mode" onClick={handleCloseUserMenu}>
                  <FormControlLabel
                  value="Dark Mode"
                  control={<Checkbox />}
                  label="Dark Mode"
                  labelPlacement="end"
                />
                </MenuItem>
              <MenuItem key="Enable Localstorage" onClick={handleCloseUserMenu}>
                  <FormControlLabel
                  value="Enable Localstorage"
                  control={<Checkbox />}
                  label="Enable Localstorage"
                  labelPlacement="end"
                />
                </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};
export default ResponsiveAppBar;