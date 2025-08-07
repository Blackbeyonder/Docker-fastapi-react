import { useEffect, useState, useRef } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { AppViewModel } from './ViewModels/AppViewModel';
import { useMap } from 'react-leaflet';


function App() {

  const {
    currentPosition, setCurrentPosition,
    getAllUbications,
    moving,
    mapRef

  } = AppViewModel();

  useEffect(() => {
    getAllUbications()

  }, []);

  



  return (
    <>
      <div className='container1'>
        <div>
          <div style={{ height: '80vh', width: "100vw" }}>
            <MapContainer center={currentPosition}
             zoom={17}
              style={{ height: '100%' }}
              ref={mapRef}
               whenCreated={(map) => {
                  mapRef.current = map;
                  // Forzar actualización del mapa después de cargar
                  setTimeout(() => map.invalidateSize(), 0);
                }}
              >
              <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
              <Marker position={currentPosition}>
                <Popup>Puntero</Popup>
              </Marker>
            </MapContainer>
          </div>
        </div>
        <div className='container2'>
          <button className="btn" onClick={moving}>Simular tracking</button>

        </div>
      </div>



    </>
  )
}

export default App
