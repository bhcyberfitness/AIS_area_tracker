import React, { createContext, useState, useEffect } from 'react';

export const VesselsContext = createContext();

export const VesselsProvider = ({ children }) => {
	const [vessels, setVessels] = useState([]);

/* 	useEffect(() => {
		fetch("http://localhost:8000/vessels")
			.then(response => response.json())
			.then(data => setVessels(data))
			.catch(error => console.error("Error fetching vessels:", error));
	}, []); */

	const fetchVessels = async () => {
		try {
			const response = await fetch(`http://localhost:8000/vessels`);
			const data = await response.json();
			setVessels(data);
		} catch (error) {
			console.error('Error fetching vessels: ', error);
		}
	};

	useEffect(() => {
		fetchVessels();
		const intervalId = setInterval(fetchVessels, 5000);

		return () => clearInterval(intervalId);
	}, []);

	const updateVessel = async (mmsi, threat) => {
		try {
			const response = await fetch(`http://localhost:8000/vessels/${mmsi}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({threat}),
			});

			const data = await response.json();

			if (response.ok) {
				setVessels(prevVessels =>
					prevVessels.map(vessel =>
						vessel.mmsi === mmsi ? { ...vessel, threat } : vessel
					)
				);
				console.log(data.data);
			} else {
				console.error(data.data);
			}
		} catch (error) {
			console.error('Error updating vessel:', error);
		}
	};

	return (
		<VesselsContext.Provider value={{ vessels, setVessels, updateVessel }}>
			{children}
		</VesselsContext.Provider>
	);
};