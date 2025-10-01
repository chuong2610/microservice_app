import React from 'react';
import { getAppConfig } from '../config/appConfig';

const MetaFieldForm = ({ metaFields, onChange }) => {
  const appConfig = getAppConfig();

  const handleFieldChange = (fieldName, value) => {
    onChange({
      ...metaFields,
      [fieldName]: value
    });
  };

  const renderField = (field) => {
    const value = metaFields[field.name] || '';

    switch (field.type) {
      case 'textarea':
        return (
          <textarea
            id={field.name}
            value={value}
            onChange={(e) => handleFieldChange(field.name, e.target.value)}
            className="input-field"
            rows={3}
            placeholder={`Enter ${field.label.toLowerCase()}`}
            required={field.required}
          />
        );

      case 'number':
        return (
          <input
            type="number"
            id={field.name}
            value={value}
            onChange={(e) => handleFieldChange(field.name, e.target.value)}
            className="input-field"
            placeholder={`Enter ${field.label.toLowerCase()}`}
            required={field.required}
            min={field.min}
            max={field.max}
            step={field.step}
          />
        );

      case 'boolean':
        return (
          <div className="flex items-center">
            <input
              type="checkbox"
              id={field.name}
              checked={value === true || value === 'true'}
              onChange={(e) => handleFieldChange(field.name, e.target.checked)}
              className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
            />
            <label htmlFor={field.name} className="ml-2 text-sm text-gray-700">
              {field.label}
            </label>
          </div>
        );

      case 'select':
        return (
          <select
            id={field.name}
            value={value}
            onChange={(e) => handleFieldChange(field.name, e.target.value)}
            className="input-field"
            required={field.required}
          >
            <option value="">Select {field.label.toLowerCase()}</option>
            {field.options?.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        );

      case 'datetime-local':
        return (
          <input
            type="datetime-local"
            id={field.name}
            value={value}
            onChange={(e) => handleFieldChange(field.name, e.target.value)}
            className="input-field"
            required={field.required}
          />
        );

      default:
        return (
          <input
            type="text"
            id={field.name}
            value={value}
            onChange={(e) => handleFieldChange(field.name, e.target.value)}
            className="input-field"
            placeholder={`Enter ${field.label.toLowerCase()}`}
            required={field.required}
          />
        );
    }
  };

  if (!appConfig.metaFields || appConfig.metaFields.length === 0) {
    return null;
  }

  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-2">
        <h3 className="text-lg font-medium text-gray-900">
          {appConfig.name} Specific Fields
        </h3>
        <p className="text-sm text-gray-600">
          Additional fields specific to {appConfig.name.toLowerCase()}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {appConfig.metaFields.map((field) => (
          <div key={field.name}>
            <label
              htmlFor={field.name}
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              {field.label}
              {field.required && <span className="text-red-500 ml-1">*</span>}
            </label>
            {renderField(field)}
          </div>
        ))}
      </div>
    </div>
  );
};

export default MetaFieldForm;


