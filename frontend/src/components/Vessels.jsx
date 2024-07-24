import React, { useContext, useEffect, useState } from "react";
import {
	Box,
	Button,
	Card,
	CardBody,
	CardFooter,
	CardHeader,
	Flex,
	FormControl,
	FormLabel,
	Heading,
	Input,
	InputGroup,
	Modal,
	ModalBody,
	ModalCloseButton,
	ModalContent,
	ModalFooter,
	ModalHeader,
	ModalOverlay,
	Select,
	SimpleGrid,
	Stack,
	Text,
	useDisclosure
} from "@chakra-ui/react";
import { VesselsContext } from "./VesselsContext";

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
	const { vessels, updateVessel } = useContext(VesselsContext);
	const { isOpen, onOpen, onClose } = useDisclosure();
	const [selectedVessel, setSelectedVessel] = useState(null);
	const [threat, setThreat] = useState('');

	const handleUpdateClick = (vessel) => {
		setSelectedVessel(vessel);
		setThreat(vessel.threat || '');
		onOpen();
	};

	const handleSubmit = () => {
		if (selectedVessel) {
			updateVessel(selectedVessel.mmsi, threat);
			onClose();
		}
	};

	const getCardStyle = (threat) => {
		switch (threat) {
			case 'blue':
				return { bg: 'blue.500', opacity: 0.6 };
			case 'white':
				return { bg: 'gray.300', opacity: 1 };
			case 'red':
				return { bg: 'red.500', opacity: 1 };
					
		}
	};

	return (
		<Box bg="gray.700" minH="100vh" p={5}>
{/* 		  <ul>
			{vessels.map((vessel) => (
			  <li key={vessel.mmsi}>
				{vessel.name} - Lat: {vessel.lat.toFixed(3)}, Long: {vessel.long.toFixed(3)}, Threat: {vessel.threat}
				<Button onClick={() => handleUpdateClick(vessel)} ml={4}>
				  Update Threat
				</Button>
			  </li>
			))}
		  </ul> */}

			<SimpleGrid columns={{ sm: 2, md: 4, lg: 6}} spacing={5}>
				{vessels.map((vessel) => (
					<Card
						key={vessel.mmsi}
						borderwidth="1px"
						borderRadius="lg"
						{...getCardStyle(vessel.threat)}
					>
						<CardHeader>
							<Heading size="md">{vessel.name}</Heading>
						</CardHeader>
						<CardBody>
							<Text>Lat: {vessel.lat.toFixed(3)}</Text>
							<Text>Long: {vessel.long.toFixed(3)}</Text>
							<Text>Threat Level: {vessel.threat}</Text>
						</CardBody>
						<CardFooter>
							<Button onClick={() => handleUpdateClick(vessel)} colorScheme="teal">Update Threat</Button>
						</CardFooter>
					</Card>
				))}
			</SimpleGrid>
	
		  <Modal isOpen={isOpen} onClose={onClose}>
			<ModalOverlay />
			<ModalContent>
			  <ModalHeader>Update Vessel Threat</ModalHeader>
			  <ModalCloseButton />
			  <ModalBody>
				<FormControl>
				  <FormLabel>Threat Level</FormLabel>
				  <Select
					placeholder="Select threat level"
					value={threat}
					onChange={(e) => setThreat(e.target.value)}
				  >
					<option value="blue">Blue</option>
					<option value="white">White</option>
					<option value="red">Red</option>
				  </Select>
				</FormControl>
			  </ModalBody>
	
			  <ModalFooter>
				<Button colorScheme="blue" mr={3} onClick={handleSubmit}>
				  Update
				</Button>
				<Button variant="ghost" onClick={onClose}>Cancel</Button>
			  </ModalFooter>
			</ModalContent>
		  </Modal>
		</Box>
	  );
};

export default Vessels;