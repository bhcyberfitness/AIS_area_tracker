import React, { useEffect, useState } from "react";
import {
	Box,
	Button,
    Flex,
    Input,
    InputGroup,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    Stack,
    Text,
    useDisclosure
} from "@chakra-ui/react";

/* const VesselsContext = React.createContext({
	vessels: [], fetchVessels: () => {}
})

export default function Vessels() {
	const [vessels, setVessels] = useState([])
	const fetchVessels = async () => {
		const response = await fetch("http://localhost:8000/vessels")
		const vessels = await response.json()
		setVessels(vessels.data)
	}
	useEffect(() => {
		fetchVessels()
	}, [])
	
	return (
		<VesselsContext.Provider value={{vessels, fetchVessels}}>
			<Stack spacing={5}>
				{vessels.map((vessel) => (
					<b>{vessel.name}</b>
				))}
			</Stack>
		</VesselsContext.Provider>
	)
} */

const Vessels = () => {
	const [vessels, setVessels] = useState([]);

	useEffect(() => {
		fetch("http://localhost:8000/vessels")
			.then(response => response.json())
			.then(data => setVessels(data))
			.catch(error => console.error("Error fetching vessels:", error));
	}, []);

	return (
		<Stack spacing={5}>
			<ul>
				{vessels.map(vessel => (
					<li key={vessel.mmsi}>{vessel.name} - Lat: {vessel.lat.toFixed(2)}, Long: {vessel.long.toFixed(2)}</li>
				))}
			</ul>
		</Stack>
	);
};

export default Vessels;