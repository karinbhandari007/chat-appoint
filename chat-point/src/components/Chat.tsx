import React, { useEffect, useState } from "react";
import { v4 as uuidv4 } from "uuid";
import {
  Box,
  Button,
  Input,
  Text,
  VStack,
  HStack,
  Heading,
  useToast,
  Spinner,
  Image,
} from "@chakra-ui/react";

const clientId = localStorage.getItem("clientId") || uuidv4();
if (!localStorage.getItem("clientId")) {
  localStorage.setItem("clientId", clientId);
}

const Chat: React.FC = () => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState<string>("");
  const [context, setContext] = useState({
    vaccineType: "",
    location: "",
    date: "",
    time: "",
    specialRequirements: "",
  });
  const [isTyping, setIsTyping] = useState(false);
  const toast = useToast();

  useEffect(() => {
    const newSocket = new WebSocket(
      `ws://localhost:8000/api/chat/ws/${clientId}`
    );
    if (!newSocket) return;

    setSocket(newSocket);

    newSocket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, message]);

      if (message.type === "ai_response") {
        setContext((prev) => ({
          ...prev,
          vaccineType: message.extracted_info.vaccine_type || prev.vaccineType,
          location: message.extracted_info.location || prev.location,
          date: message.extracted_info.datetime || prev.date,
        }));

        if (message?.requires_followup) {
          // toast({
          //   title: "Follow-Up Required",
          //   description: "Please provide the missing information.",
          //   status: "info",
          //   duration: 5000,
          //   isClosable: true,
          // });
        }
      }

      if (message.type === "ai_typing") {
        setIsTyping(true);
      } else {
        setIsTyping(false);
      }
    };

    newSocket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    return () => {
      if (newSocket) {
        newSocket.close();
      }
    };
  }, []);

  const sendMessage = () => {
    if (socket) {
      const patientMessage = { type: "patient", message: input };
      setMessages((prevMessages) => [...prevMessages, patientMessage]);

      socket.send(JSON.stringify({ message: input, context }));
      setInput("");
    }
  };

  const renderClinics = (clinics: any[]) => {
    return clinics.map((clinicData, index) => (
      <Box
        key={index}
        borderWidth={1}
        borderRadius="md"
        p={3}
        mb={2}
        bg="gray.100"
      >
        <Text fontWeight="bold">{clinicData.clinic.name}</Text>
        <Text>{clinicData.clinic.address}</Text>
        <Text>
          {clinicData.clinic.city}, {clinicData.clinic.state}{" "}
          {clinicData.clinic.zip_code}
        </Text>
        <Text>Distance: {clinicData.distance.toFixed(2)} meters</Text>
        <Text>Vaccines Offered: {clinicData.clinic.vaccines.join(", ")}</Text>
        <Text fontWeight="bold">Available Appointments:</Text>
        {clinicData.appointments.map((appointment: any) => (
          <Text key={appointment.id}>
            - {new Date(appointment.appointment_time).toLocaleString()} (Status:{" "}
            {appointment.status})
          </Text>
        ))}
      </Box>
    ));
  };

  return (
    <Box height="100vh" display="flex" flexDirection="column" bg="gray.50">
      <Box
        p={5}
        borderWidth={1}
        boxShadow="md"
        color="white"
        position="relative"
      >
        <Image
          src="https://cdn.prod.website-files.com/62eb4217467fa543d7f2ba2b/62f1fb8937f05da2d202199c_Logo.svg"
          height={50}
        />
        <Box
          position="absolute"
          width="100%"
          display="flex"
          flexDirection="row"
          justifyContent="center"
          top="6"
        >
          <Heading as="h2" size="lg" mb={4} color="black">
            AI-Powered Appointment Scheduling
          </Heading>
        </Box>
      </Box>

      <VStack spacing={4} align="stretch" flex="1" overflow="hidden" px={4}>
        <Box
          borderWidth={1}
          borderRadius="md"
          p={3}
          overflowY="auto"
          bg="white"
          flex="1"
          boxShadow="sm"
          maxHeight="80vh"
        >
          {messages.map((msg, index) => (
            <HStack
              key={index}
              justifyContent={
                msg.type !== "patient" ? "flex-start" : "flex-end"
              }
              mb={2}
            >
              <Text
                color={msg.type !== "patient" ? "blue.500" : "black"}
                bg={msg.type !== "patient" ? "gray.200" : "teal.100"}
                borderRadius="md"
                p={3}
                maxWidth="70%"
                textAlign={msg.type !== "patient" ? "left" : "right"}
                fontSize="sm"
                boxShadow="md"
              >
                <strong>{msg.type !== "patient" ? "AI" : "You"}:</strong>{" "}
                {msg.type === "ai_response" ? (
                  <div>
                    <div
                      dangerouslySetInnerHTML={{
                        __html: msg?.message?.response ?? msg?.message,
                      }}
                    />
                    {!!msg?.available_clinics?.length && (
                      <div>
                        <strong>Available Clinics:</strong>
                        {renderClinics(msg?.available_clinics)}
                      </div>
                    )}
                  </div>
                ) : (
                  msg?.message?.response ?? msg?.message
                )}
              </Text>
            </HStack>
          ))}
          {isTyping && (
            <HStack justifyContent="flex-start" mb={2}>
              <Text color="gray.500">AI is typing...</Text>
              <Spinner size="sm" />
            </HStack>
          )}
        </Box>

        <HStack spacing={4} align="center">
          <Input
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
            size="lg"
            bg="white"
            borderColor="teal.500"
            borderRadius="lg"
            boxShadow="sm"
          />
          <Button
            colorScheme="teal"
            onClick={sendMessage}
            size="lg"
            isLoading={isTyping}
            loadingText="Sending"
          >
            Send
          </Button>
        </HStack>
      </VStack>
    </Box>
  );
};

export default Chat;
