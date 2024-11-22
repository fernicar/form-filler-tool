const fetchServer = async () => {
  const url = "http://localhost:8080";
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });
  return response.json();
};
