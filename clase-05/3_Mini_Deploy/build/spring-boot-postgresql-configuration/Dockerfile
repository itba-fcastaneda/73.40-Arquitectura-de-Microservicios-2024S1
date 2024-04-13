  FROM maven:3.8.4-openjdk-17-slim AS build

  # Set the working directory
  WORKDIR /app

  # Copy the pom.xml file to the working directory
  COPY pom.xml .

  # Download the project dependencies
  RUN mvn dependency:go-offline -B

  # Copy the source code to the working directory
  COPY src ./src

  # Build the application
  RUN mvn package -DskipTests

  # Use a lightweight base image with Java installed
  FROM openjdk:17-jdk-slim

  # Set the working directory
  WORKDIR /app

  # Copy the built JAR file from the previous stage
  COPY --from=build /app/target/*.jar app.jar

  # Expose the application port
  EXPOSE 8080

  # Run the application
  CMD ["java", "-jar", "app.jar"]
  