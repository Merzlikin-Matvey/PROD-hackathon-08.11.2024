import React, { useState, useEffect } from "react";
import "./event_block.css";

interface EventBlockProps {
  title: string;
  startDate: string;
  endDate: string;
  data: Record<string, string>;
  // eslint-disable-next-line
  onUpdate: (updatedEvent: any) => void;
  uuid: string;
}

const EventBlock: React.FC<EventBlockProps> = ({ uuid, title, startDate, endDate, data, onUpdate }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState(title);
  const [editedStartDate, setEditedStartDate] = useState(startDate);
  const [editedEndDate, setEditedEndDate] = useState(endDate);
  const [editedData, setEditedData] = useState(data);

  useEffect(() => {
    setEditedTitle(title);
    setEditedStartDate(startDate);
    setEditedEndDate(endDate);
    setEditedData(data);
  }, [title, startDate, endDate, data]);

  const handleSave = () => {
    onUpdate({
      name: editedTitle,
      startDate: editedStartDate,
      endDate: editedEndDate,
      data: editedData,
      event_uuid: uuid
    });
    setIsEditing(false);
  };

  return (
      <div className="event-block">
        {isEditing ? (
            <>
              <input
                  type="text"
                  value={editedTitle}
                  onChange={(e) => setEditedTitle(e.target.value)}
              />
              <br/>
              <br/>
              <input
                  type="datetime-local"
                  value={editedStartDate}
                  onChange={(e) => setEditedStartDate(e.target.value)}
              />
              <br/>
              <br/>
              <input
                  type="datetime-local"
                  value={editedEndDate}
                  onChange={(e) => setEditedEndDate(e.target.value)}
              />
              <br/>
              <br/>
              {Object.entries(editedData).map(([key, value]) => (
                  <input
                      key={key}
                      type="text"
                      value={value}
                      onChange={(e) => setEditedData({ ...editedData, [key]: e.target.value })}
                  />
              ))}
              <br/>
              <br/>
              <button onClick={handleSave}>Сохранить</button>
            </>
        ) : (
            <>
              <h2>{title}</h2>
              <p>Дата начала: {startDate}</p>
              <p>Дата окончания: {endDate}</p>
              {Object.entries(data).map(([key, value]) => (
                  <p key={key}>{`${key}: ${value}`}</p>
              ))}
              <button onClick={() => setIsEditing(true)}>Редактировать</button>
            </>
        )}
      </div>
  );
};

export default EventBlock;