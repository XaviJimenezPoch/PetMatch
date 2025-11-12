import React from "react";
import { Box, Button, Typography } from "@mui/material";
import PetsIcon from "@mui/icons-material/Pets";
import gatImatgeInfEsq from "../../assets/gat-cantonada.png"; // ✅ Import la imatge
import gatImatgeSupDreta from "../../assets/gat-superior.png";
import gosImatgeCentre from "../../assets/gos-baix.png";

export default function Landpage() {
  return (
    <Box
      sx={{
        minHeight: "90vh",
        minWidth: "100vw",
        bgcolor: "#f5e0c3",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "flex-start",
        paddingTop: 15,
        gap: 4,
        position: "relative",
      }}
    >
        <Box
        component="img"
        src={gatImatgeSupDreta} 
        alt="Gato siamés"
        sx={{
          position: "absolute",
          top: 0,
          right: 0,
          width: 300,
          height: "auto",
        //   borderRadius: 2,
          objectFit: "cover",
        }}
      />
      {/* Títol amb icona */}
      <Box display="flex" alignItems="center" gap={1}>
        <PetsIcon sx={{ color: "#f5842b", fontSize: 100 }} />
        <Typography className="custom-title"
          variant="h1"
          sx={{
            fontFamily: "'Rubik Bubbles', sans-serif",

          }}
        > 
          AdoptApp
        </Typography>
      </Box>

      {/* Botons */}
      <Box display="flex" flexDirection="column" gap={2}>
        <Button
          variant="contained"
          sx={{
            bgcolor: "#66c5bd",
            "&:hover": { bgcolor: "#29afa4ff" },
            borderRadius: 5,
            px: 4,
            fontSize: "1.1rem",
          }}
        >
          Iniciar sessió
        </Button>

        <Button
          variant="contained"
          sx={{
            bgcolor: "#f5842b",
            "&:hover": { bgcolor: "#fc6d00ff" },
            borderRadius: 5,
            px: 4,
            fontSize: "1.1rem",
          }}
        >
          Registrar-se
        </Button>
      </Box>
        <Box
        component="img"
        src={gatImatgeInfEsq} // Canvia per la teva imatge
        alt="Gato siamés"
        sx={{
          position: "absolute",
          bottom: 0,
          left: 0,
          width: 300,
          height: "auto",
        //   borderRadius: 2,
          objectFit: "cover",
        }}
      />
       <Box
        component="img"
        src={gosImatgeCentre} // Canvia per la teva imatge
        alt="Gato siamés"
        sx={{
          position: "absolute",
          bottom: 0,
          left: "50",
          width: 250,
          height: "auto",
        //   borderRadius: 2,
          objectFit: "cover",
        }}
      />
    </Box>
  );
}