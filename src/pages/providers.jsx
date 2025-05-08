import React from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  ExternalLink,
  Shield,
  HeartPulse,
  Home,
  Building,
  Briefcase,
  UserCheck,
  Globe,
  Banknote,
} from "lucide-react";

export const providers = [
  {
    id: 1,
    title: "Life Insurance Corporation of India (LIC)",
    description:
      "LIC is one of the oldest and most trusted insurance providers in India, offering a wide range of life insurance products. Known for its extensive network and government backing.",
    website: "https://www.licindia.in/",
    icon: Shield,
    rating: 4.5,
  },
  {
    id: 2,
    title: "HDFC Life Insurance",
    description:
      "HDFC Life is a leading private life insurance company in India, known for its innovative products and customer service. Offers a variety of life insurance plans including term, endowment, and ULIPs.",
    website: "https://www.hdfclife.com/",
    icon: HeartPulse,
    rating: 4.4,
  },
  {
    id: 3,
    title: "ICICI Prudential Life Insurance",
    description:
      "ICICI Prudential Life Insurance offers a comprehensive range of life insurance products. Known for its strong digital presence and wide range of policies catering to various needs.",
    website: "https://www.iciciprulife.com/",
    icon: UserCheck,
    rating: 4.3,
  },
  {
    id: 4,
    title: "Max Life Insurance",
    description:
      "Max Life provides a range of life insurance products including term, whole life, and investment plans. Known for its customer-centric approach and strong financial stability.",
    website: "https://www.maxlifeinsurance.com/",
    icon: Briefcase,
    rating: 4.2,
  },
  {
    id: 5,
    title: "Bajaj Allianz General Insurance",
    description:
      "Bajaj Allianz offers a variety of general insurance products including health, motor, and property insurance. Known for its customer service and wide range of offerings.",
    website: "https://www.bajajallianz.com/",
    icon: Globe,
    rating: 4.1,
  },
  {
    id: 6,
    title: "Star Health & Allied Insurance",
    description:
      "Star Health specializes in health insurance products and is known for its extensive network of hospitals and customer-friendly policies.",
    website: "https://www.starhealth.in/",
    icon: HeartPulse,
    rating: 4.0,
  },
  {
    id: 7,
    title: "Tata AIG General Insurance",
    description:
      "Tata AIG offers a wide range of general insurance products including motor, travel, and health insurance. Known for its reliability and customer service.",
    website: "https://www.tataaig.com/",
    icon: Shield,
    rating: 4.0,
  },
  {
    id: 8,
    title: "New India Assurance",
    description:
      "New India Assurance is a government-owned general insurance company providing a variety of insurance products including health, motor, and property insurance.",
    website: "https://newindia.co.in/",
    icon: Building,
    rating: 3.9,
  },
  {
    id: 9,
    title: "Reliance General Insurance",
    description:
      "Reliance General offers a range of general insurance products including health, motor, and home insurance. Known for its extensive branch network and digital services.",
    website: "https://www.reliancegeneral.co.in/",
    icon: Banknote,
    rating: 3.8,
  },
  {
    id: 10,
    title: "HDFC Ergo General Insurance",
    description:
      "HDFC Ergo provides a wide range of general insurance products such as health, motor, and travel insurance. Known for its innovative solutions and customer-centric approach.",
    website: "https://www.hdfcergo.com/",
    icon: Home,
    rating: 3.7,
  },
];

const Providers = () => {
  return (
    <div className="container mx-auto max-w-7xl px-4 py-12">
      <div className="text-center mb-12">
        <h1 className="text-3xl font-bold text-blue-900 mb-4 dark:text-blue-400">
          Insurance Providers Directory
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto dark:text-gray-400">
          Browse our network of trusted insurance providers. Use your
          personalized quote to negotiate better rates.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {providers.map((provider) => (
          <Card
            key={provider.id}
            className="border-gray-200 hover:shadow-md transition-shadow dark:border-gray-800"
          >
            <CardHeader className="pb-2">
              <div className="h-16 flex items-center justify-center mb-2">
              <provider.icon className="w-10 h-10 text-blue-600" />
              </div>
              <CardTitle className="text-xl text-blue-900 dark:text-blue-400">
                {provider.title}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-gray-700 min-h-[80px] dark:text-gray-300">
                {provider.description}
              </CardDescription>
            </CardContent>
            <CardFooter className="flex flex-col sm:flex-row gap-2">
              <a
                href={provider.website}
                target="_blank"
                rel="noopener noreferrer"
                className="w-full sm:w-auto"
              >
                <Button
                  variant="outline"
                  className="w-full sm:w-auto border-blue-300 text-blue-700 hover:bg-blue-50 dark:border-blue-800 dark:text-blue-400 dark:hover:bg-blue-950"
                >
                  <ExternalLink className="mr-2 h-4 w-4" />
                  Visit Website
                </Button>
              </a>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Providers;
