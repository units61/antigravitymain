"use client";

import React, { useCallback } from "react";
import useEmblaCarousel from "embla-carousel-react";
import Autoplay from "embla-carousel-autoplay";
import { Star, Quote, ChevronLeft, ChevronRight } from "lucide-react";

/**
 * TestimonialCarousel Component
 * 
 * Adapted from Embla Carousel headless layout pattern.
 * Creates an aesthetic card slider for customer testimonials with native dragging,
 * autoplay interval plugin, and manual nav triggers.
 */
export default function TestimonialCarousel({ title, subtitle, items = [], colors, motion_config }) {
  // Initialize Embla with custom loop and Autoplay plugins
  const [emblaRef, emblaApi] = useEmblaCarousel(
    { loop: true, align: "center", skipSnaps: false },
    [Autoplay({ delay: 5000, stopOnInteraction: false })]
  );

  const defaultItems = [
    {
      name: "Marcus Vance",
      role: "Creative Director, Studio Nine",
      quote: "ANDIP completely transformed our layout workflow. The ability to express structural concepts and receive visual masterpieces with advanced GSAP physics is absolutely mind-blowing.",
      avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=150&auto=format&fit=crop"
    },
    {
      name: "Elena Rostova",
      role: "Lead Frontend Engineer, VeloX",
      quote: "The visual output is incredible. The generated code is clean, utilizes semantic design variables, and matches premium Awwwards-tier standards without bloat. Lenis scroll feels like butter.",
      avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=150&auto=format&fit=crop"
    },
    {
      name: "Siddharth Mehta",
      role: "VP of Product, Apex Digital",
      quote: "I was skeptical of layout generation tools, but ANDIP is on another level. The bento grid configurations and GSAP scroll reveal mechanisms are flawless. Truly outstanding aesthetic execution.",
      avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=150&auto=format&fit=crop"
    }
  ];

  const testimonials = items && items.length > 0 ? items : defaultItems;

  const scrollPrev = useCallback(() => {
    if (emblaApi) emblaApi.scrollPrev();
  }, [emblaApi]);

  const scrollNext = useCallback(() => {
    if (emblaApi) emblaApi.scrollNext();
  }, [emblaApi]);

  return (
    <section className="relative py-24 px-6 md:px-12 w-full bg-background border-b border-borderColor overflow-hidden">
      {/* Decorative backdrop blobs */}
      <div className="absolute top-0 right-0 w-[30vw] h-[30vw] rounded-full bg-accent/5 filter blur-[100px] pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-[25vw] h-[25vw] rounded-full bg-muted/5 filter blur-[80px] pointer-events-none" />

      <div className="max-w-6xl mx-auto relative z-10">
        {(title || subtitle) && (
          <div className="mb-16 text-center max-w-2xl mx-auto">
            {title && (
              <h2 className="text-3xl md:text-5xl font-header font-extrabold tracking-tight text-foreground mb-4">
                {title}
              </h2>
            )}
            {subtitle && (
              <p className="text-base md:text-lg font-body font-light text-foreground/70">
                {subtitle}
              </p>
            )}
          </div>
        )}

        {/* Slider viewport */}
        <div className="overflow-hidden cursor-grab active:cursor-grabbing" ref={emblaRef}>
          <div className="flex">
            {testimonials.map((item, idx) => (
              <div key={`testimonial-${idx}`} className="flex-[0_0_100%] min-w-0 px-2 md:px-12 flex justify-center">
                <div className="max-w-3xl w-full bg-card border border-borderColor rounded-custom p-8 md:p-14 shadow-xl flex flex-col items-center text-center relative overflow-hidden">
                  {/* Styled oversized background quote symbol */}
                  <Quote className="w-20 h-20 text-accent/5 absolute top-6 left-6 pointer-events-none" />
                  
                  {/* Star Rating indicators */}
                  <div className="flex gap-1 mb-6 text-accent">
                    {[...Array(5)].map((_, i) => (
                      <Star key={`star-${i}`} className="w-4 h-4 fill-accent text-accent" />
                    ))}
                  </div>

                  {/* Testimonial Statement */}
                  <p className="text-lg md:text-2xl font-body font-light text-foreground/80 mb-8 leading-relaxed italic">
                    "{item.quote || item.description}"
                  </p>

                  {/* Profile Header */}
                  <div className="flex items-center gap-4 mt-2">
                    {item.avatar && (
                      <img
                        src={item.avatar}
                        alt={item.name}
                        className="w-14 h-14 rounded-full border border-accent/20 object-cover shadow-md"
                      />
                    )}
                    <div className="text-left">
                      <h4 className="font-header font-bold text-foreground text-base md:text-lg">
                        {item.name}
                      </h4>
                      <p className="font-body text-xs md:text-sm text-foreground/50 font-light">
                        {item.role || item.subtitle}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Carousel Manual Controls */}
        <div className="flex justify-center gap-4 mt-10">
          <button
            onClick={scrollPrev}
            className="p-3.5 rounded-full border border-borderColor text-foreground/75 hover:border-accent hover:text-accent hover:bg-accent/5 active:scale-95 transition-all duration-300 outline-none"
            aria-label="Previous slide"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <button
            onClick={scrollNext}
            className="p-3.5 rounded-full border border-borderColor text-foreground/75 hover:border-accent hover:text-accent hover:bg-accent/5 active:scale-95 transition-all duration-300 outline-none"
            aria-label="Next slide"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </section>
  );
}
