# ---------------------------------------------------------------------


import unittest
from protoclass import proto, clone


# ---------------------------------------------------------------------


class TestProto(unittest.TestCase):
    def test_proto(self):
        # members
        mikan = proto(name="mikan")
        self.assertEqual(mikan.name, "mikan")
        mikan.color = "orange"
        self.assertEqual(mikan.color, "orange")
        mikan.type = "fruit"
        self.assertEqual(mikan.type, "fruit")
        # methods
        mikan.__str__ = lambda self: self.name
        self.assertEqual(str(mikan), mikan.name)
        self.assertEqual(mikan.__str__(), mikan.name)
        mikan.introduce = lambda self: f"watashi wa {self.name} desu!"
        self.assertEqual(mikan.introduce(), "watashi wa mikan desu!")

    def test_chain_members(self):
        # basic object creation
        orenji = proto(name="orenji")
        self.assertEqual(orenji.name, "orenji")
        # assure propragation from parents to children
        orange_fruit = proto(color="orange")
        self.assertEqual(orange_fruit.color, "orange")
        # old object
        orenji.chain(orange_fruit)
        self.assertEqual(orenji.color, "orange")
        orenji = orenji.chain(orange_fruit)
        self.assertEqual(orenji.name, "orenji")
        self.assertEqual(orenji.color, "orange")
        # new object
        mikan = proto(name="mikan").chain(orange_fruit)
        self.assertEqual(mikan.name, "mikan")
        self.assertEqual(mikan.color, "orange")
        # assure that children mask parents' values
        orange_fruit.name = "orange_fruit"
        self.assertEqual(orange_fruit.name, "orange_fruit")
        self.assertEqual(orenji.name, "orenji")
        self.assertEqual(mikan.name, "mikan")
        # assure that children do not modify parents or siblings
        mikan.color = "orange-brown"
        self.assertEqual(mikan.color, "orange-brown")
        self.assertEqual(orenji.color, "orange")
        self.assertEqual(orange_fruit.color, "orange")
        # assure that parents can be changed
        orange_fruit.fruit_type = "ripe"
        brown_fruit = proto(color="brown")
        orenji.chain(brown_fruit)
        self.assertEqual(orenji.color, "brown")
        try:
            orenji.fruit_type  # not present in current prototype
            self.assertTrue(False)
        except AttributeError:
            self.assertTrue(True)
        brown_fruit.fruit_type = "rotten"
        self.assertEqual(brown_fruit.fruit_type, "rotten")
        self.assertEqual(orenji.fruit_type, "rotten")

    def test_chain_methods(self):
        # basic object creation
        ringo = proto(en="apple")
        self.assertEqual(ringo.en, "apple")
        # update method of parent
        furutsu = proto(en="fruit")
        ringo = ringo.chain(furutsu)
        self.assertNotEqual(str(furutsu), "fruit")
        self.assertNotEqual(str(ringo), "apple")
        # new functionality
        furutsu.__str__ = lambda self: self.en
        self.assertEqual(str(furutsu), "fruit")
        self.assertEqual(str(ringo), "apple")
        # update method of child
        ringo.__str__ = lambda self: f"I am {self.en}"
        self.assertEqual(furutsu.__str__(), "fruit")
        self.assertEqual(ringo.__str__(), "I am apple")

    def test_clone(self):
        # base object
        animal = proto(kind="animal")
        self.assertEqual(animal.kind, "animal")
        # a simple clone
        cat = clone(animal)
        self.assertEqual(cat.kind, "animal")
        # a clone of a clone
        kitten = clone(cat)
        kitten.size = "small"
        self.assertEqual(kitten.kind, "animal")
        self.assertEqual(kitten.size, "small")
        # propagation
        cat.greet = lambda self: "meow"
        self.assertEqual(kitten.greet(), "meow")

    def test_chain_self(self):
        try:
            katze = proto(name="klin")
            katze = katze.chain(katze)  # chaining self is not allowed
            self.assertTrue(False)
        except TypeError:
            self.assertTrue(True)

    def test_clone_self(self):
        katze = proto(name="klin")
        katze = clone(katze)  # cloning creates a new object
        katze.size = "small"
        self.assertEqual(katze.name, "klin")
        self.assertEqual(katze.size, "small")


if __name__ == "__main__":
    unittest.main()