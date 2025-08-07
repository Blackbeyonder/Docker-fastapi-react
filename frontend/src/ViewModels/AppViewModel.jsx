import React, { useEffect, useRef, useState } from 'react';
import SimuladorService from '../services/SimuladorService';


export const AppViewModel = () => {



    const [currentPosition, setCurrentPosition] = useState([20.969562, -89.68994]);
    const [allUbications, setAllUbications] = useState(
        [
            {
                "lat": 20.969562,
                "lng": -89.68994
            },
            {
                "lat": 20.969693,
                "lng": -89.689928
            },
            {
                "lat": 20.97006,
                "lng": -89.689892
            },
            {
                "lat": 20.970327,
                "lng": -89.689862
            },
            {
                "lat": 20.970362,
                "lng": -89.689858
            },
            {
                "lat": 20.970653,
                "lng": -89.689815
            },
            {
                "lat": 20.971511,
                "lng": -89.689687
            },
            {
                "lat": 20.971928,
                "lng": -89.689705
            },
            {
                "lat": 20.972433,
                "lng": -89.689731
            },
            {
                "lat": 20.973319,
                "lng": -89.689623
            },
            {
                "lat": 20.9737,
                "lng": -89.68957
            },
            {
                "lat": 20.974877,
                "lng": -89.689398
            },
            {
                "lat": 20.975579,
                "lng": -89.689275
            },
            {
                "lat": 20.975954,
                "lng": -89.689135
            },
            {
                "lat": 20.976231,
                "lng": -89.689012
            },
            {
                "lat": 20.976425,
                "lng": -89.688904
            },
            {
                "lat": 20.97661,
                "lng": -89.68877
            },
            {
                "lat": 20.976745,
                "lng": -89.688647
            },
            {
                "lat": 20.976856,
                "lng": -89.688518
            },
            {
                "lat": 20.976991,
                "lng": -89.688325
            },
            {
                "lat": 20.977126,
                "lng": -89.688126
            },
            {
                "lat": 20.977367,
                "lng": -89.687745
            },
            {
                "lat": 20.977948,
                "lng": -89.686687
            },
            {
                "lat": 20.979547,
                "lng": -89.683863
            },
            {
                "lat": 20.97988,
                "lng": -89.683431
            },
            {
                "lat": 20.98022,
                "lng": -89.683116
            },
            {
                "lat": 20.98072,
                "lng": -89.682732
            },
            {
                "lat": 20.98258,
                "lng": -89.681524
            },
            {
                "lat": 20.983817,
                "lng": -89.68073
            },
            {
                "lat": 20.984404,
                "lng": -89.680331
            },
            {
                "lat": 20.987054,
                "lng": -89.678602
            },
            {
                "lat": 20.990315,
                "lng": -89.676462
            },
            {
                "lat": 20.990513,
                "lng": -89.676329
            },
            {
                "lat": 20.992731,
                "lng": -89.674899
            },
            {
                "lat": 20.994988,
                "lng": -89.673431
            },
            {
                "lat": 20.995975,
                "lng": -89.672794
            },
            {
                "lat": 20.998155,
                "lng": -89.671373
            },
            {
                "lat": 20.999288,
                "lng": -89.670655
            },
            {
                "lat": 20.999759,
                "lng": -89.670152
            },
            {
                "lat": 21.000081,
                "lng": -89.669945
            },
            {
                "lat": 21.000187,
                "lng": -89.669873
            },
            {
                "lat": 21.000549,
                "lng": -89.669651
            },
            {
                "lat": 21.00122,
                "lng": -89.669205
            },
            {
                "lat": 21.001227,
                "lng": -89.668772
            },
            {
                "lat": 21.001267,
                "lng": -89.66817
            },
            {
                "lat": 21.001352,
                "lng": -89.667062
            },
            {
                "lat": 21.001432,
                "lng": -89.666016
            },
            {
                "lat": 21.001532,
                "lng": -89.665023
            },
            {
                "lat": 21.001535,
                "lng": -89.664992
            },
            {
                "lat": 21.000916,
                "lng": -89.664792
            },
            {
                "lat": 21.000659,
                "lng": -89.664709
            },
            {
                "lat": 21.0003,
                "lng": -89.664593
            },
            {
                "lat": 20.999684,
                "lng": -89.664396
            },
            {
                "lat": 20.999051,
                "lng": -89.664191
            },
            {
                "lat": 20.998424,
                "lng": -89.663975
            },
            {
                "lat": 20.9983,
                "lng": -89.663937
            },
            {
                "lat": 20.998285,
                "lng": -89.663829
            },
            {
                "lat": 20.998271,
                "lng": -89.663751
            },
            {
                "lat": 20.998205,
                "lng": -89.663565
            },
            {
                "lat": 20.998157,
                "lng": -89.663428
            },
            {
                "lat": 20.998087,
                "lng": -89.663232
            },
            {
                "lat": 20.997713,
                "lng": -89.662161
            },
            {
                "lat": 20.997675,
                "lng": -89.662056
            },
            {
                "lat": 20.997743,
                "lng": -89.66199
            },
            {
                "lat": 20.997879,
                "lng": -89.661919
            },
            {
                "lat": 20.997951,
                "lng": -89.661819
            },
            {
                "lat": 20.998189,
                "lng": -89.661488
            },
            {
                "lat": 20.998271,
                "lng": -89.661375
            },
            {
                "lat": 20.998467,
                "lng": -89.661102
            },
            {
                "lat": 20.998593,
                "lng": -89.660927
            },
            {
                "lat": 20.998747,
                "lng": -89.660713
            },
            {
                "lat": 20.998916,
                "lng": -89.660479
            },
            {
                "lat": 20.999003,
                "lng": -89.660357
            },
            {
                "lat": 20.999278,
                "lng": -89.659976
            },
            {
                "lat": 20.999407,
                "lng": -89.659796
            },
            {
                "lat": 20.999602,
                "lng": -89.659526
            },
            {
                "lat": 20.999177,
                "lng": -89.658393
            },
            {
                "lat": 20.99875,
                "lng": -89.65706
            },
            {
                "lat": 20.998329,
                "lng": -89.655792
            },
            {
                "lat": 20.997857,
                "lng": -89.654491
            },
            {
                "lat": 20.997646,
                "lng": -89.653799
            },
            {
                "lat": 20.997439,
                "lng": -89.653154
            },
            {
                "lat": 20.997433,
                "lng": -89.653136
            },
            {
                "lat": 20.997303,
                "lng": -89.652751
            },
            {
                "lat": 20.9971,
                "lng": -89.652145
            },
            {
                "lat": 20.996767,
                "lng": -89.651151
            },
            {
                "lat": 20.996479,
                "lng": -89.650305
            },
            {
                "lat": 20.996031,
                "lng": -89.649003
            },
            {
                "lat": 20.995602,
                "lng": -89.64774
            },
            {
                "lat": 20.995582,
                "lng": -89.64765
            },
            {
                "lat": 20.995583,
                "lng": -89.647591
            },
            {
                "lat": 20.995584,
                "lng": -89.647531
            },
            {
                "lat": 20.995582,
                "lng": -89.646288
            },
            {
                "lat": 20.995582,
                "lng": -89.646235
            },
            {
                "lat": 20.995545,
                "lng": -89.645698
            },
            {
                "lat": 20.99545,
                "lng": -89.644634
            },
            {
                "lat": 20.995355,
                "lng": -89.64358
            },
            {
                "lat": 20.995324,
                "lng": -89.64314
            },
            {
                "lat": 20.995259,
                "lng": -89.642535
            },
            {
                "lat": 20.995189,
                "lng": -89.641689
            },
            {
                "lat": 20.995133,
                "lng": -89.640844
            },
            {
                "lat": 20.995112,
                "lng": -89.640573
            },
            {
                "lat": 20.99509,
                "lng": -89.640347
            },
            {
                "lat": 20.99507,
                "lng": -89.640106
            },
            {
                "lat": 20.995063,
                "lng": -89.640021
            },
            {
                "lat": 20.994992,
                "lng": -89.639133
            },
            {
                "lat": 20.994914,
                "lng": -89.638274
            },
            {
                "lat": 20.994827,
                "lng": -89.637303
            },
            {
                "lat": 20.994733,
                "lng": -89.636368
            },
            {
                "lat": 20.994715,
                "lng": -89.636242
            },
            {
                "lat": 20.994783,
                "lng": -89.636176
            },
            {
                "lat": 20.994884,
                "lng": -89.636067
            },
            {
                "lat": 20.995237,
                "lng": -89.635685
            },
            {
                "lat": 20.995718,
                "lng": -89.63514
            },
            {
                "lat": 20.996889,
                "lng": -89.633781
            },
            {
                "lat": 20.997005,
                "lng": -89.633631
            },
            {
                "lat": 20.997106,
                "lng": -89.633447
            },
            {
                "lat": 20.997156,
                "lng": -89.633309
            },
            {
                "lat": 20.997167,
                "lng": -89.633279
            },
            {
                "lat": 20.997226,
                "lng": -89.633106
            },
            {
                "lat": 20.99728,
                "lng": -89.632841
            },
            {
                "lat": 20.997285,
                "lng": -89.632803
            },
            {
                "lat": 20.9973,
                "lng": -89.63261
            },
            {
                "lat": 20.997298,
                "lng": -89.632226
            },
            {
                "lat": 20.997297,
                "lng": -89.632132
            },
            {
                "lat": 20.997239,
                "lng": -89.629804
            },
            {
                "lat": 20.997238,
                "lng": -89.629716
            },
            {
                "lat": 20.997247,
                "lng": -89.628388
            },
            {
                "lat": 20.997225,
                "lng": -89.627676
            },
            {
                "lat": 20.997205,
                "lng": -89.627006
            },
            {
                "lat": 20.997202,
                "lng": -89.626775
            },
            {
                "lat": 20.997219,
                "lng": -89.625721
            },
            {
                "lat": 20.997219,
                "lng": -89.625653
            },
            {
                "lat": 20.997201,
                "lng": -89.624999
            },
            {
                "lat": 20.997198,
                "lng": -89.624391
            },
            {
                "lat": 20.99718,
                "lng": -89.623483
            },
            {
                "lat": 20.997181,
                "lng": -89.623399
            },
            {
                "lat": 20.997177,
                "lng": -89.623235
            },
            {
                "lat": 20.997149,
                "lng": -89.622973
            },
            {
                "lat": 20.997115,
                "lng": -89.622784
            },
            {
                "lat": 20.997096,
                "lng": -89.622677
            },
            {
                "lat": 20.99702,
                "lng": -89.622456
            },
            {
                "lat": 20.996989,
                "lng": -89.622387
            },
            {
                "lat": 20.996931,
                "lng": -89.622258
            },
            {
                "lat": 20.996504,
                "lng": -89.621528
            },
            {
                "lat": 20.996463,
                "lng": -89.621487
            },
            {
                "lat": 20.9964,
                "lng": -89.621446
            },
            {
                "lat": 20.996311,
                "lng": -89.621392
            },
            {
                "lat": 20.996277,
                "lng": -89.621382
            },
            {
                "lat": 20.996246,
                "lng": -89.621367
            },
            {
                "lat": 20.996218,
                "lng": -89.621346
            },
            {
                "lat": 20.996189,
                "lng": -89.621313
            },
            {
                "lat": 20.996168,
                "lng": -89.621274
            },
            {
                "lat": 20.996155,
                "lng": -89.621231
            },
            {
                "lat": 20.996152,
                "lng": -89.621186
            },
            {
                "lat": 20.996157,
                "lng": -89.621141
            },
            {
                "lat": 20.996172,
                "lng": -89.621099
            },
            {
                "lat": 20.996186,
                "lng": -89.621075
            },
            {
                "lat": 20.996202,
                "lng": -89.621054
            },
            {
                "lat": 20.996212,
                "lng": -89.621043
            },
            {
                "lat": 20.996223,
                "lng": -89.621032
            },
            {
                "lat": 20.996234,
                "lng": -89.621023
            },
            {
                "lat": 20.996246,
                "lng": -89.621015
            },
            {
                "lat": 20.996257,
                "lng": -89.621009
            },
            {
                "lat": 20.996287,
                "lng": -89.620996
            },
            {
                "lat": 20.996318,
                "lng": -89.620989
            },
            {
                "lat": 20.99635,
                "lng": -89.620988
            },
            {
                "lat": 20.996381,
                "lng": -89.620992
            },
            {
                "lat": 20.996411,
                "lng": -89.621002
            },
            {
                "lat": 20.996439,
                "lng": -89.621017
            },
            {
                "lat": 20.996465,
                "lng": -89.621036
            },
            {
                "lat": 20.996485,
                "lng": -89.621058
            },
            {
                "lat": 20.996575,
                "lng": -89.621108
            },
            {
                "lat": 20.996642,
                "lng": -89.621133
            },
            {
                "lat": 20.997236,
                "lng": -89.621239
            },
            {
                "lat": 20.997237,
                "lng": -89.621239
            },
            {
                "lat": 20.997456,
                "lng": -89.621296
            },
            {
                "lat": 20.99781,
                "lng": -89.62141
            },
            {
                "lat": 20.997885,
                "lng": -89.621435
            },
            {
                "lat": 20.997976,
                "lng": -89.621459
            },
            {
                "lat": 20.998106,
                "lng": -89.621487
            },
            {
                "lat": 20.998197,
                "lng": -89.621502
            },
            {
                "lat": 20.998961,
                "lng": -89.621631
            }
        ]
    )

    const wsShipment = useRef(null);
    const mapRef = useRef();

    const getAllUbications = async () => {

        const response = await SimuladorService.getUbicaciones();
        if (response.data.status && response.data.status == 200) {
            let info = response.data.data;
            const last = info[info.length - 1];

            setCurrentPosition([last.latitud, last.longitud])
            conectarWebSocketShipment()

        }

    };

    function getMexicoIsoTimestamp() {
        const now = new Date();
        const tzOffsetMin = -now.getTimezoneOffset();  // por ejemplo +360 para UTC−6h
        const sign = tzOffsetMin >= 0 ? '+' : '-';
        const pad = n => String(Math.floor(Math.abs(n))).padStart(2, '0');
        const hours = pad(tzOffsetMin / 60);
        const minutes = pad(tzOffsetMin % 60);
        const iso = now.toISOString().replace('Z', '');
        return `${iso}${sign}${hours}:${minutes}`;
    }


    const moving = async () => {

        try {

            const found = allUbications.findIndex(item =>
                item.lat === currentPosition[0] && item.lng === currentPosition[1]
            );

            if (found !== -1) {
                const nextIndex = found + 1;
                if (nextIndex < allUbications.length) {
                    let nextPosition = allUbications[nextIndex];


                    const timestampMexico = getMexicoIsoTimestamp();
                    let data = {
                        "latitud": nextPosition.lat,
                        "longitud": nextPosition.lng,
                        "timestamp": timestampMexico
                    }


                    const responseGuadar = await SimuladorService.postGuardarUbicaciones(data)
                    if (responseGuadar.data.status && responseGuadar.data.status == 200) {
                        setCurrentPosition([nextPosition.lat, nextPosition.lng]);
                        if (mapRef.current) {
                            mapRef.current.flyTo([nextPosition.lat, nextPosition.lng], mapRef.current.getZoom());
                        }
                    }
                }

            }

            console.log('Índice encontrado:', found);


        } catch (error) {
            console.log(error);


        }


    };

    const conectarWebSocketShipment = () => {

        if (wsShipment.current &&
            (wsShipment.current.readyState === WebSocket.OPEN ||
                wsShipment.current.readyState === WebSocket.CONNECTING)) {
            // Ya está conectado o conectándose
            return;
        }

        const roomId = `salaMonitoreo`;
        const WEB_SOCKET_URL = import.meta.env.VITE_WEB_SOCKET_URL;

        const ws = new WebSocket(`${WEB_SOCKET_URL}/${roomId}`);


        ws.onopen = () => {
            console.log(`Conectado a la sala: ${roomId}`);
        };
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log("Mensaje recibido:", data);
            let newInfo = data.data;
            if (newInfo) {
                setCurrentPosition([newInfo.latitud, newInfo.longitud])

            }

        };
        ws.onerror = (error) => console.error("WebSocket error:", error);
        ws.onclose = (ev) => {
            console.log(`Desconectado de ${roomId}`, ev.reason);
        };

        wsShipment.current = ws;

    };




    return {
        currentPosition, setCurrentPosition,
        getAllUbications,
        moving,
        mapRef

    };
};
