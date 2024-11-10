"use client";
import React, { useState } from "react";
import "./style.css";
import { useRouter } from "next/navigation";

export default function AddTour() {
  const [name, setName] = useState("");
  const [country, setCountry] = useState("");
  const router = useRouter();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const response = await fetch("/api/add_tour", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, country }),
    });
    if (response.ok) {
      alert("Мероприятие успешно добавлено!");
      router.push("/tours");
    } else {
      alert("Ошибка при добавлении мероприятия.");
    }
  };

  return (
      <div className="form-container">
        <h1 id="mini_label">Добавить тур</h1>
        <form onSubmit={handleSubmit}>
          <label>
            Название:
            <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
            />
          </label>
          <label>
            Страна:
            <input
                type="text"
                value={country}
                onChange={(e) => setCountry(e.target.value)}
                required
            />
          </label>
          <button type="submit">Отправить</button>
        </form>
      </div>
  );
}